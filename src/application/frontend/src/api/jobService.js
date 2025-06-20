// src/api/jobService.js

// import { jobsData } from '../mockData';

// Hàm này giả lập việc gọi API để lấy danh sách công việc
// src/api/jobService.js
const API_BASE_URL = "/api/v1"; 
// const API_BASE_URL = "http://joblytics.io.vn/api/v1"; // Hoặc URL API của bạn

/**
 * Fetches jobs from the API.
 * @param {object} [params] - Optional parameters for filtering jobs.
 * @param {string} [params.searchTerm] - The search term for job titles, descriptions, etc.
 * @param {string} [params.location] - The location to search for jobs.
 * @returns {Promise<Array<object>>} A promise that resolves to an array of job objects.
 * @throws {Error} If the network response is not ok.
 */
export const getJobs = async (params) => {
  let url = `${API_BASE_URL}/jobs`;

  if (params && (params.searchTerm || params.location)) {
    const queryParams = new URLSearchParams();
    if (params.searchTerm) {
      // Đảm bảo tên tham số 'searchTerm' khớp với những gì backend mong đợi
      // Ví dụ: có thể là 'q', 'title', 'search', v.v.
      queryParams.append("searchTerm", params.searchTerm);
    }
    if (params.location) {
      queryParams.append("location", params.location);
    }
    url += `?${queryParams.toString()}`;
  }

  console.log("Fetching jobs from URL:", url); // Để debug

  try {
    const response = await fetch(url);
    if (!response.ok) {
      // Nếu server trả về lỗi, cố gắng parse lỗi nếu có body JSON
      let errorData;
      try {
        errorData = await response.json();
      } catch (e) {
        // Không có body JSON hoặc không parse được
        errorData = { message: response.statusText };
      }
      throw new Error(
        `HTTP error! status: ${response.status}, message: ${
          errorData.message || response.statusText
        }`
      );
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error in getJobs:", error);
    // Ném lại lỗi để component gọi có thể xử lý
    // Hoặc bạn có thể trả về một giá trị mặc định như mảng rỗng tùy theo yêu cầu
    throw error;
    // return []; // Hoặc trả về mảng rỗng nếu muốn component không bị crash
  }
};

/**
 * Fetches distinct seniority levels from the API.
 * @returns {Promise<Array<string>>} A promise that resolves to an array of seniority levels.
 * @throws {Error} If the network response is not ok.
 */
export const getSeniorities = async () => {
  const url = `${API_BASE_URL}/seniorities`; // Replace with your actual endpoint
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error in getSeniorities:", error);
    // You might want to return a default value or re-throw the error
    return []; // Or throw error;
  }
};

/**
 * Fetches job title suggestions from the API.
 * @param {string} query - The search query for job titles.
 * @returns {Promise<Array<string>>} A promise that resolves to an array of job title strings.
 */
export const getJobTitleSuggestions = async (query) => {
  if (!query || query.trim() === "") {
    return [];
  }
  // Backend endpoint này cần được tạo: ví dụ /api/v1/job-title-suggestions
  const url = `${API_BASE_URL}/job-title-suggestions?query=${encodeURIComponent(
    query.trim()
  )}`;
  try {
    const response = await fetch(url);
    if (!response.ok) {
      console.error(
        `HTTP error fetching job title suggestions! status: ${response.status}`
      );
      return []; // Trả về mảng rỗng khi có lỗi để UI không bị crash
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error in getJobTitleSuggestions:", error);
    return []; // Trả về mảng rỗng khi có lỗi
  }
};

/**
 * Fetches location suggestions from the API.
 * @param {string} query - The search query for locations.
 * @returns {Promise<Array<string>>} A promise that resolves to an array of location strings.
 */
export const getLocationSuggestions = async (query) => {
  if (!query || query.trim() === "") {
    return [];
  }
  // Backend endpoint này cần được tạo: ví dụ /api/v1/location-suggestions
  const url = `${API_BASE_URL}/location-suggestions?query=${encodeURIComponent(
    query.trim()
  )}`;
  try {
    const response = await fetch(url);
    if (!response.ok) {
      console.error(
        `HTTP error fetching location suggestions! status: ${response.status}`
      );
      return [];
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error in getLocationSuggestions:", error);
    return [];
  }
};

// Bạn có thể thêm các hàm API khác ở đây, ví dụ:
// export const getJobById = async (id) => { ... };
// export const createJob = async (jobData) => { ... };
