import axios from "axios";

// Create axios instance
const api = axios.create({
    baseURL: "http://localhost:5000/api",
});

// Add a request interceptor to include the session ID
api.interceptors.request.use(
    (config) => {
        const sessionId = localStorage.getItem("sessionId");
        if (sessionId) {
            config.headers["X-Session-Id"] = sessionId;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

export const getConfig = async () => {
    try {
        const response = await api.get("/config");
        return response.data;
    } catch (error) {
        throw error.response ? error.response.data : error;
    }
};

export const getAllPapers = async () => {
    try {
        const response = await api.get("/papers");
        return response.data;
    } catch (error) {
        throw error.response ? error.response.data : error;
    }
};

export const getPaperById = async (id) => {
    try {
        const response = await api.get(`/papers/${id}`);
        return response.data;
    } catch (error) {
        throw error.response ? error.response.data : error;
    }
};

export const generatePaper = async (data) => {
    try {
        const response = await api.post("/papers/generate", data);
        return response.data;
    } catch (error) {
        throw error.response ? error.response.data : error;
    }
};

export const uploadFile = async (file, subject) => {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("subject", subject);

    try {
        const response = await api.post("/upload", formData, {
            headers: {
                "Content-Type": "multipart/form-data",
            },
        });
        return response.data;
    } catch (error) {
        throw error.response ? error.response.data : error;
    }
};

export const updatePaper = async (id, data) => {
    try {
        const response = await api.put(`/papers/${id}`, data);
        return response.data;
    } catch (error) {
        throw error.response ? error.response.data : error;
    }
};

export const downloadPaperPDF = async (id) => {
    try {
        const response = await api.get(`/papers/${id}/download`, {
            responseType: 'blob'
        });
        
        // Create a link element to trigger the download
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        
        // Extract filename from header if possible, else use default
        const contentDisposition = response.headers['content-disposition'];
        let filename = `Paper_${id}.pdf`;
        if (contentDisposition) {
            const filenameMatch = contentDisposition.match(/filename="?(.+)"?/i);
            if (filenameMatch.length > 1) {
                filename = filenameMatch[1];
            }
        }
        
        link.setAttribute('download', filename);
        document.body.appendChild(link);
        link.click();
        
        // Cleanup
        link.remove();
        window.URL.revokeObjectURL(url);
    } catch (error) {
        throw error.response ? error.response.data : error;
    }
};

export default {
    getConfig,
    getAllPapers,
    getPaperById,
    generatePaper,
    uploadFile,
    updatePaper,
    downloadPaperPDF
};
