import { API } from "aws-amplify";
import axios from "axios";

export class ApiRequest {
  static async get<T>(
    path: string,
    params?: {
      [key: string]: any;
    },
    headers?: {
      [key: string]: any;
    }
  ): Promise<T[] | null> {
    const apiName = "sbc-api";
    // const path = "/users";
    const myInit = {
      headers: headers, // OPTIONAL
      response: false, // OPTIONAL (return the entire Axios response object instead of only response.data)
      queryStringParameters: {},
      //    {
      //   name: "param", // OPTIONAL
      // },
    };

    if (params) {
      myInit.queryStringParameters = params;
    }

    return axios
      .get(`${import.meta.env.VITE_SBC_API_URL}/${path}`, { params })
      .then((response) => {
        return response.data.data as T;
        // Add your code here
      })
      .catch((error) => {
        console.error(error.response);

        return null;
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

  static async delete<T>(
    path: string,
    params?: {
      [key: string]: any;
    },
    headers?: {
      [key: string]: any;
    }
  ): Promise<T | null> {
    const apiName = "sbc-api";
    // const path = "/users";
    const myInit = {
      headers: headers, // OPTIONAL
      response: false, // OPTIONAL (return the entire Axios response object instead of only response.data)
      queryStringParameters: {},
      //    {
      //   name: "param", // OPTIONAL
      // },
    };

    if (params) {
      myInit.queryStringParameters = params;
    }

    return API.del(apiName, `/${path}`, myInit)
      .then((response) => {
        return response.data as T;
        // Add your code here
      })
      .catch((error) => {
        console.error(error.response);

        return null;
      });
  }

  static async post<T>(
    path: string,
    body: T | any,
    params?: {
      [key: string]: any;
    },
    headers?: {
      [key: string]: any;
    }
  ): Promise<T[] | null> {
    const apiName = "sbc-api";
    // const path = "/users";
    const myInit = {
      headers: headers, // OPTIONAL
      response: false, // OPTIONAL (return the entire Axios response object instead of only response.data)
      body: body,
      queryStringParameters: {},
      //    {
      //   name: "param", // OPTIONAL
      // },
    };

    if (params) {
      myInit.queryStringParameters = params;
    }

    return API.post(apiName, `/${path}`, myInit).then((response) => {
      return response.data as T[];
      // Add your code here
    });
  }

  static async put<T>(
    path: string,
    body: T | any,
    params?: {
      [key: string]: any;
    },
    headers?: {
      [key: string]: any;
    }
  ): Promise<T[] | null> {
    const apiName = "sbc-api";
    // const path = "/users";
    const myInit = {
      headers: headers, // OPTIONAL
      response: false, // OPTIONAL (return the entire Axios response object instead of only response.data)
      body: body,
      queryStringParameters: {},
      //    {
      //   name: "param", // OPTIONAL
      // },
    };

    if (params) {
      myInit.queryStringParameters = params;
    }

    return API.put(apiName, `/${path}`, myInit).then((response) => {
      return response.data as T[];
      // Add your code here
    });
    // .catch((error) => {
    //   console.log(error.response);

    //   return null;
    // });
  }
}
