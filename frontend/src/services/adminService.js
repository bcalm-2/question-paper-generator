import api from "./api";

export const getAdminSubjects = async () => {
    const response = await api.get("/admin/subjects");
    return response.data;
};

export const addSubject = async (data) => {
    const response = await api.post("/admin/subjects", data);
    return response.data;
};

export const deleteSubject = async (id) => {
    const response = await api.delete(`/admin/subjects/${id}`);
    return response.data;
};

export const getAdminFiles = async () => {
    const response = await api.get("/admin/files");
    return response.data;
};

export const deleteFile = async (filename) => {
    const response = await api.delete(`/admin/files/${filename}`);
    return response.data;
};

export default {
    getAdminSubjects,
    addSubject,
    deleteSubject,
    getAdminFiles,
    deleteFile
};
