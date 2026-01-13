// API Configuration
const API_BASE_URL = 'http://localhost:8000/api';

// Helper function để gọi API
async function apiCall(endpoint, method = 'GET', data = null) {
    try {
        const options = {
            method: method,
            headers: {
                'Content-Type': 'application/json',
            }
        };
        
        if (data) {
            options.body = JSON.stringify(data);
        }
        
        const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
        
        if (!response.ok) {
            throw new Error(`API Error: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API Call Error:', error);
        throw error;
    }
}

// ==================== CROPS API ====================
const CropsAPI = {
    // Lấy danh sách mùa vụ
    async getAll() {
        return await apiCall('/crops/');
    },
    
    // Lấy chi tiết mùa vụ
    async getById(id) {
        return await apiCall(`/crops/${id}`);
    },
    
    // Tạo mùa vụ mới
    async create(cropData) {
        return await apiCall('/crops/', 'POST', cropData);
    },
    
    // Cập nhật mùa vụ
    async update(id, cropData) {
        return await apiCall(`/crops/${id}`, 'PUT', cropData);
    },
    
    // Xóa mùa vụ
    async delete(id) {
        return await apiCall(`/crops/${id}`, 'DELETE');
    }
};

// ==================== WEATHER API ====================
const WeatherAPI = {
    // Lấy thời tiết hiện tại
    async getCurrent(lat, lon) {
        return await apiCall(`/weather/current?lat=${lat}&lon=${lon}`);
    },
    
    // Lấy dự báo thời tiết
    async getForecast(lat, lon, days = 7) {
        return await apiCall(`/weather/forecast?lat=${lat}&lon=${lon}&days=${days}`);
    },
    
    // Lấy lịch sử thời tiết của mùa vụ
    async getByCrop(cropId) {
        return await apiCall(`/weather/crop/${cropId}`);
    }
};

// ==================== CARE LOGS API ====================
const CareLogsAPI = {
    // Tạo nhật ký chăm sóc
    async create(careLogData) {
        return await apiCall('/care-logs/', 'POST', careLogData);
    },
    
    // Lấy nhật ký chăm sóc của mùa vụ
    async getByCrop(cropId) {
        return await apiCall(`/care-logs/crop/${cropId}`);
    }
};

// ==================== PESTS API ====================
const PestsAPI = {
    // Nhận diện sâu bệnh
    async identify(pestData) {
        return await apiCall('/pests/identify', 'POST', pestData);
    },
    
    // Lấy lịch sử nhận diện
    async getByCrop(cropId) {
        return await apiCall(`/pests/crop/${cropId}`);
    }
};

// ==================== ANALYTICS API ====================
const AnalyticsAPI = {
    // Tính SHI
    async getSHI(cropId) {
        return await apiCall(`/analytics/shi/${cropId}`);
    },
    
    // Tổng hợp thông tin mùa vụ
    async getCropSummary(cropId) {
        return await apiCall(`/analytics/crop/${cropId}/summary`);
    },
    
    // Lịch sử mùa vụ
    async getSeasonHistory(cropId) {
        return await apiCall(`/analytics/season-history/${cropId}`);
    }
};

// ==================== AI ASSISTANT API ====================
const AIAssistantAPI = {
    // Hỏi trợ lý AI
    async ask(question, cropId = null) {
        return await apiCall('/ai/ask', 'POST', {
            question: question,
            crop_id: cropId
        });
    }
};

