import { useUserStore } from "@/stores/user";
import { API } from "aws-amplify";
import axios from "axios";

export class ApiRequest {
  static async get<T>(path: string): Promise<T[] | null> {
    return axios
      .get(`${import.meta.env.VITE_SBC_API_URL}/${path}`, {
        withCredentials: true,
        headers: {
          Authorization: `Bearer ${useUserStore().token}`,
        },
      })
      .then((response) => {
        return response.data.data as T[];
        // Add your code here
      });

    // return API.get(apiName, `/${path}`, myInit)
    // .then((response) => {
    //   return response.data as T;
    //   // Add your code here
    // })
    // .catch((error) => {
    //   console.error(error.response);

    //   return null;
    // });
  }

  static async delete<T>(path: string): Promise<T[] | null> {
    return axios
      .delete(`${import.meta.env.VITE_SBC_API_URL}/${path}`, {
        headers: {
          Authorization: `Bearer ${useUserStore().token}`,
        },
        withCredentials: true,
      })
      .then((response) => {
        return response.data.data as T[];
        // Add your code here
      });
  }

  static async post<T>(path: string, body: T | any): Promise<T[] | null> {
    return axios
      .post(`${import.meta.env.VITE_SBC_API_URL}/${path}`, body, {
        headers: {
          Authorization: `Bearer ${useUserStore().token}`,
        },
      })
      .then((response) => {
        return response.data.data as T[];
      });
  }

  static async put<T>(path: string, body: T | any): Promise<T[] | null> {
    return axios
      .put(`${import.meta.env.VITE_SBC_API_URL}/${path}`, body, {
        headers: {
          Authorization: `Bearer ${useUserStore().token}`,
        },
      })
      .then((response) => {
        return response.data.data as T[];
      });
  }
}
