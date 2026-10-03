import axios from "axios";

const client = axios.create({
    baseURL: "http://localhost:5000/api",
    timeout: 600000,
});

export default client;