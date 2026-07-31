import client from "./client";

export async function getDashboard() {
    const response = await client.get("/dashboard");
    return response.data;
}