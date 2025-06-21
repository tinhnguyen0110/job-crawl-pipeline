// src/pages/JobSearchPage/components/JobList.jsx
import React from 'react';
import JobListItem from './JobListItem';

function JobList({ jobs, onJobSelect, selectedJobId }) {
  return (
    <div className="job-list">
      {jobs.map(job => (
        <JobListItem 
          key={job.id} 
          job={job} 
          onSelect={onJobSelect}
          isSelected={job.id === selectedJobId}
        />
      ))}
    </div>
  );
}

export default JobList;