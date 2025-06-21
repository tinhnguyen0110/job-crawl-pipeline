// src/pages/JobSearchPage/JobSearchPage.jsx

import React, { useState, useEffect } from 'react';
import { getJobs } from '../../api/jobService';
import { isMobileBreakpoint } from '../../utils/deviceUtils';

import JobList from './components/JobList';
import JobDetails from './components/JobDetails';
import SearchBar from './components/SearchBar';
import Pagination from './components/Pagination';

import './JobSearchPage.css';

function JobSearchPage() {
  const [jobs, setJobs] = useState([]);
  const [selectedJob, setSelectedJob] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const [showJobDetail, setShowJobDetail] = useState(false);
  const [isSearching, setIsSearching] = useState(false);
  const [searchParams, setSearchParams] = useState({ searchTerm: '', location: '', seniority: '' });
  const [isMobile, setIsMobile] = useState(isMobileBreakpoint());
  const itemsPerPage = 5;

  // Calculate pagination values
  const indexOfLastJob = currentPage * itemsPerPage;
  const indexOfFirstJob = indexOfLastJob - itemsPerPage;
  const currentJobs = jobs.slice(indexOfFirstJob, indexOfLastJob);
  const totalPages = Math.ceil(jobs.length / itemsPerPage);

  const loadInitialJobs = async () => {
    setIsLoading(true);
    setIsSearching(false);
    setSearchParams({ searchTerm: '', location: '', seniority: '' });
    try {
      const data = await getJobs();
      setJobs(data || []);
      if (data && data.length > 0) {
        setSelectedJob(data[0]);
      } else {
        setSelectedJob(null);
      }
    } catch (error) {
      console.error("Error fetching initial jobs:", error);
      setJobs([]);
      setSelectedJob(null);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadInitialJobs();
  }, []);

  useEffect(() => {
    const handleResize = () => {
      const newIsMobile = isMobileBreakpoint();
      setIsMobile(newIsMobile);
      
      if (!newIsMobile && showJobDetail) {
        setShowJobDetail(false);
      }
    };

    window.addEventListener('resize', handleResize);
    
    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, [showJobDetail, selectedJob, jobs.length]);

  const handleJobSelect = (job) => {
    setSelectedJob(job);
    if (isMobile) {
      setShowJobDetail(true);
    }
  };

  const handleBackToList = () => {
    setShowJobDetail(false);
    setSelectedJob(null);
  };

  const handlePageChange = (pageNumber) => {
    setCurrentPage(pageNumber);
    const newIndexOfFirstJob = (pageNumber - 1) * itemsPerPage;
    const firstJobOnPage = jobs[newIndexOfFirstJob];
    if (firstJobOnPage) {
      setSelectedJob(firstJobOnPage);
    } else {
      setSelectedJob(null);
    }
    window.scrollTo(0, 0);
  };

  const handleSearch = (searchTerm, location, seniority) => {
    const trimmedSearchTerm = searchTerm.trim();
    const trimmedSeniority = seniority;
    const trimmedLocation = location.trim();

    if (isMobile && showJobDetail) {
      setShowJobDetail(false);
    }

    if (trimmedSearchTerm === "" && trimmedLocation === "" && trimmedSeniority === "") {
      loadInitialJobs();
    } else {
      const performSearch = async () => {
        setIsLoading(true);
        setCurrentPage(1);
        setIsSearching(true);
        setSearchParams({ 
          searchTerm: trimmedSearchTerm, 
          location: trimmedLocation, 
          seniority: trimmedSeniority 
        });
        try {
          const params = {};
          if (trimmedSearchTerm !== "") {
            params.searchTerm = trimmedSearchTerm;
          }
          if (trimmedLocation !== "") {
            params.location = trimmedLocation;
          }
          if (trimmedSeniority !== "") {
            params.seniority = trimmedSeniority;
          }
          const data = await getJobs(params);
          setJobs(data || []);
          if (data && data.length > 0) {
            setSelectedJob(data[0]);
          } else {
            setSelectedJob(null);
          }
        } catch (error) {
          console.error("Error searching jobs:", error);
          setJobs([]);
          setSelectedJob(null);
        } finally {
          setIsLoading(false);
        }
      };
      performSearch();
    }
  };


  const EmptyJobList = () => {
    const hasSearchTerms = isSearching && (searchParams.searchTerm || searchParams.location || searchParams.seniority);
    
    return (
      <div className="empty-job-list">
        <div className="empty-content">
          <i className={hasSearchTerms ? "fas fa-search" : "fas fa-briefcase"}></i>
          <h3>{hasSearchTerms ? "Không tìm thấy công việc phù hợp" : "Chưa có công việc nào"}</h3>
          <p>
            {hasSearchTerms 
              ? `Không tìm thấy công việc phù hợp với từ khóa "${searchParams.searchTerm || searchParams.location || searchParams.seniority}". Hãy thử tìm kiếm với từ khóa khác.`
              : "Hiện tại chưa có công việc nào được đăng tuyển. Vui lòng quay lại sau."
            }
          </p>
        </div>
      </div>
    );
  };

  return (
    <div className="page-container">
      <div className="sticky-header">
        <div className="site-header">
          <div className="header-left">
            <button className="notification-btn">
              <i className="fas fa-bell"></i>
              Thông báo việc làm
            </button>
          </div>
          
          <div className="header-center">
            <h1 className="site-title">Joblytics.io.vn</h1>
            <p className="site-subtitle">Tìm kiếm công việc mơ ước của bạn</p>
          </div>

          <div className="header-right">
            <button className="login-btn">
              <i className="fas fa-user"></i>
              Đăng nhập
            </button>
          </div>
        </div>
        <SearchBar onSearch={handleSearch} />
      </div>
      <main className="main-content">
        {isLoading ? (
          <div className="loading-spinner">Loading...</div>
        ) : jobs.length === 0 ? (
          <EmptyJobList />
        ) : (
          <>

            {isMobile && showJobDetail ? (
              <div className="mobile-job-detail">
                <button className="back-to-list-btn" onClick={handleBackToList}>
                  <i className="fas fa-arrow-left"></i>
                  Quay lại danh sách
                </button>
                <JobDetails job={selectedJob} />
              </div>
            ) : (
              <div className="job-list-container">
                <JobList
                  jobs={currentJobs}
                  onJobSelect={handleJobSelect}
                  selectedJobId={selectedJob?.id}
                />
                <Pagination
                  currentPage={currentPage}
                  totalPages={totalPages}
                  onPageChange={handlePageChange}
                />
              </div>
            )}

            {!isMobile && <JobDetails job={selectedJob} />}
          </>
        )}
      </main>
    </div>
  );
}

export default JobSearchPage;