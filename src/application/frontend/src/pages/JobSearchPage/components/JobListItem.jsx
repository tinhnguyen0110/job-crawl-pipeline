// src/pages/JobSearchPage/components/JobListItem.jsx
import React from 'react';
import logoPlaceholder from '../../../assets/images/unnamed.png'; 

function truncateText(text, maxLength) {
  // Nếu text không tồn tại hoặc đã đủ ngắn, trả về nguyên bản
  if (!text || text.length <= maxLength) {
    return text;
  }
  // Nếu text quá dài, cắt ngắn và thêm "..."
  return `${text.substring(0, maxLength)}...`;
}

function JobListItem({ job, onSelect, isSelected }) {
  const itemClassName = `job-list-item ${isSelected ? 'selected' : ''}`;
  const MAX_TAG_LENGTH = 25;
  return (
    <div className={itemClassName} onClick={() => onSelect(job)}>
      {/* Sử dụng biến ảnh đã import */}
      <img src={logoPlaceholder} alt={`${job.company} logo`} className="company-logo" />
      <div className="job-info">
        <h3 className="job-title">{job.job_title}</h3>
        <p className="company-name">{job.company}</p>
        <div className="job-tags">
          {/* Logic: hiển thị text đã cắt ngắn, nhưng `title` chứa text GỐC */}
          {job.salary && (
            <span title={job.salary}> {/* <-- THÊM THUỘC TÍNH TITLE Ở ĐÂY */}
              {truncateText(job.salary, MAX_TAG_LENGTH)}
            </span>
          )}

          {job.location && (
            <span title={job.location}> {/* <-- THÊM THUỘC TÍNH TITLE Ở ĐÂY */}
              {truncateText(job.location, MAX_TAG_LENGTH)}
            </span>
          )}
          
          {job.seniority && (
            <span title={job.seniority}> {/* <-- THÊM THUỘC TÍNH TITLE Ở ĐÂY */}
              {truncateText(job.seniority, MAX_TAG_LENGTH)}
            </span>
          )}
        </div>
      </div>
    </div>
  );
}

export default JobListItem;