import google.generativeai as genai
from app.config import settings
from typing import Optional, Dict, Any
import json
import base64

class AIService:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        if self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                # Sử dụng model mới nhất có sẵn
                self.model = genai.GenerativeModel('models/gemini-2.5-flash')
            except Exception as e:
                try:
                    # Fallback về model khác nếu không có
                    self.model = genai.GenerativeModel('models/gemini-pro-latest')
                except:
                    print(f"⚠️ Lỗi khởi tạo Gemini: {e}")
                    self.model = None
        else:
            self.model = None
    
    async def identify_pest(self, description: str, crop_type: str = "coffee_robusta") -> Dict[str, Any]:
        """Nhận diện côn trùng/sâu bệnh dựa trên mô tả (Knowledge-based)"""
        if not self.model:
            return {
                "identified_pest_name": "Không thể nhận diện (API key chưa được cấu hình)",
                "confidence_score": 0.0,
                "pest_type": "unknown",
                "severity": "unknown",
                "recommendation": "Vui lòng cấu hình GEMINI_API_KEY trong file .env"
            }
        
        # Knowledge base về sâu bệnh cà phê Robusta
        knowledge_base = """
        Sâu bệnh phổ biến trên cà phê Robusta:
        1. Rầy xanh (Green leafhopper) - Empoasca spp.
        2. Sâu đục thân (Coffee stem borer) - Xylotrechus quadripes
        3. Bọ xít muỗi (Coffee berry borer) - Hypothenemus hampei
        4. Bệnh gỉ sắt (Coffee leaf rust) - Hemileia vastatrix
        5. Bệnh khô cành (Dieback) - Colletotrichum gloeosporioides
        6. Rệp sáp (Mealybugs) - Planococcus spp.
        7. Mọt đục quả (Coffee berry borer)
        """
        
        prompt = f"""
        Bạn là chuyên gia nông nghiệp về cây cà phê Robusta. 
        Dựa trên mô tả sau đây, hãy nhận diện sâu bệnh và đưa ra khuyến nghị.
        
        Kiến thức về sâu bệnh cà phê:
        {knowledge_base}
        
        Mô tả từ người dùng: {description}
        Loại cây: {crop_type}
        
        Hãy trả lời dưới dạng JSON với các trường:
        {{
            "identified_pest_name": "Tên sâu bệnh",
            "confidence_score": 0.0-1.0,
            "pest_type": "insect/disease/weed",
            "severity": "low/medium/high",
            "recommendation": "Khuyến nghị xử lý chi tiết"
        }}
        """
        
        try:
            if not self.model:
                raise Exception("Model chưa được khởi tạo")
            response = self.model.generate_content(prompt)
            # Parse JSON từ response
            text = response.text.strip()
            # Loại bỏ markdown code blocks nếu có
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()
            
            result = json.loads(text)
            return result
        except Exception as e:
            error_msg = str(e)
            print(f"Error in AI pest identification: {error_msg}")
            # Nếu lỗi về model, thử fallback
            if "404" in error_msg or "not found" in error_msg.lower():
                return {
                    "identified_pest_name": "Lỗi cấu hình model",
                    "confidence_score": 0.0,
                    "pest_type": "unknown",
                    "severity": "medium",
                    "recommendation": "Vui lòng kiểm tra lại API key và model name. Lỗi: " + error_msg[:100]
                }
            return {
                "identified_pest_name": "Không xác định được",
                "confidence_score": 0.0,
                "pest_type": "unknown",
                "severity": "medium",
                "recommendation": f"Lỗi xử lý: {error_msg[:100]}. Vui lòng mô tả chi tiết hơn."
            }
    
    async def identify_pest_from_image(self, image_base64: str, mime_type: str, crop_type: str = "coffee_robusta") -> Dict[str, Any]:
        """Nhận diện côn trùng/sâu bệnh từ ảnh sử dụng Gemini Vision"""
        if not self.model:
            return {
                "identified_pest_name": "Không thể nhận diện (API key chưa được cấu hình)",
                "confidence_score": 0.0,
                "pest_type": "unknown",
                "severity": "unknown",
                "is_beneficial": None,
                "recommendation": "Vui lòng cấu hình GEMINI_API_KEY trong file .env"
            }
        
        # Knowledge base về côn trùng có lợi và có hại
        knowledge_base = """
        Côn trùng có hại trên cà phê Robusta:
        1. Rầy xanh (Green leafhopper) - Empoasca spp. - CÓ HẠI
        2. Sâu đục thân (Coffee stem borer) - Xylotrechus quadripes - CÓ HẠI
        3. Bọ xít muỗi (Coffee berry borer) - Hypothenemus hampei - CÓ HẠI
        4. Rệp sáp (Mealybugs) - Planococcus spp. - CÓ HẠI
        5. Mọt đục quả (Coffee berry borer) - CÓ HẠI
        
        Côn trùng có lợi:
        1. Bọ rùa (Ladybugs) - Coccinellidae - CÓ LỢI (ăn rệp)
        2. Ong mật - CÓ LỢI (thụ phấn)
        3. Bọ xít ăn thịt - CÓ LỢI (ăn sâu hại)
        4. Kiến vàng - CÓ LỢI (bảo vệ cây)
        """
        
        prompt = f"""
        Bạn là chuyên gia nông nghiệp về cây cà phê Robusta. 
        Hãy phân tích ảnh côn trùng này và trả lời các câu hỏi sau:
        
        1. Đây là loại côn trùng/sâu bệnh gì? (Tên khoa học và tên thường gọi)
        2. Côn trùng này có LỢI hay có HẠI cho cây cà phê?
        3. Mức độ nghiêm trọng (low/medium/high) nếu có hại
        4. Khuyến nghị xử lý cụ thể
        
        Kiến thức về côn trùng:
        {knowledge_base}
        
        Loại cây: {crop_type}
        
        Hãy trả lời dưới dạng JSON với các trường:
        {{
            "identified_pest_name": "Tên côn trùng (tên khoa học và tên thường gọi)",
            "confidence_score": 0.0-1.0,
            "pest_type": "insect/disease/weed/beneficial",
            "is_beneficial": true/false/null,
            "severity": "low/medium/high/none",
            "affected_area": null,
            "recommendation": "Khuyến nghị chi tiết: Nếu có hại thì cách xử lý, nếu có lợi thì cách bảo vệ"
        }}
        """
        
        try:
            from PIL import Image
            import io
            
            # Decode base64 image
            image_bytes = base64.b64decode(image_base64)
            image = Image.open(io.BytesIO(image_bytes))
            
            # Gọi Gemini Vision API
            response = self.model.generate_content([prompt, image])
            
            # Parse JSON từ response
            text = response.text.strip()
            # Loại bỏ markdown code blocks nếu có
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()
            
            result = json.loads(text)
            return result
        except Exception as e:
            error_msg = str(e)
            print(f"Error in AI image identification: {error_msg}")
            return {
                "identified_pest_name": "Không xác định được",
                "confidence_score": 0.0,
                "pest_type": "unknown",
                "is_beneficial": None,
                "severity": "medium",
                "affected_area": None,
                "recommendation": f"Lỗi xử lý ảnh: {error_msg[:150]}. Vui lòng thử lại với ảnh rõ hơn."
            }
    
    async def analyze_season_data(self, season_data: Dict[str, Any], question: str) -> str:
        """Phân tích dữ liệu lịch sử mùa vụ và trả lời câu hỏi"""
        if not self.model:
            return "AI Assistant chưa được cấu hình. Vui lòng thêm GEMINI_API_KEY vào file .env"
        
        prompt = f"""
        Bạn là trợ lý AI chuyên về phân tích dữ liệu nông nghiệp.
        Dựa trên dữ liệu mùa vụ sau đây, hãy trả lời câu hỏi của người dùng.
        
        Dữ liệu mùa vụ:
        {json.dumps(season_data, indent=2, ensure_ascii=False)}
        
        Câu hỏi: {question}
        
        Hãy đưa ra câu trả lời chi tiết, có số liệu cụ thể và khuyến nghị dựa trên phân tích.
        """
        
        try:
            if not self.model:
                return "AI Assistant chưa được cấu hình. Vui lòng kiểm tra GEMINI_API_KEY trong file .env"
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            error_msg = str(e)
            if "404" in error_msg or "not found" in error_msg.lower():
                return f"Lỗi: Model Gemini không tìm thấy. Vui lòng kiểm tra API key. Chi tiết: {error_msg[:150]}"
            return f"Lỗi khi phân tích: {error_msg[:200]}"

ai_service = AIService()

