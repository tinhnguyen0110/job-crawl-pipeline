// src/pages/JobSearchPage/components/JobDetails.jsx
import React from 'react';

function JobDetails({ job }) {
  
  if (!job) {
    return <div className="job-details placeholder">Chọn một việc làm để xem chi tiết</div>;
  }

  // const { title, description } = job;

  return (
    <div className="job-details">
      <h2 className="job-detail-title">{job.job_title}</h2>
      {job.location && <p className="job-detail-location">Địa điểm: {job.location}</p>}
      {job.date_posted && <p>Ngày đăng: {job.date_posted}</p>}
      <button className="apply-button">Ứng tuyển ngay</button>

      <div className="detail-section">
        <h3>Mô tả công việc</h3>
        <ul>
          {job.job_description}
        </ul>
      </div>
      
      <div className="detail-section">
        <h3>Yêu cầu</h3>
        <ul>
          {job.job_requirements}
        </ul>
      </div>
      <div className="detail-section">
        <h3>Lương</h3>
        <ul>
          {job.salary}
        </ul>
      </div>
      
      <div className="detail-section">
        <h3>Quyền lợi</h3>
        <ul>
          {job.benefits}
        </ul>
      </div>
    </div>
  );
}

export default JobDetails;