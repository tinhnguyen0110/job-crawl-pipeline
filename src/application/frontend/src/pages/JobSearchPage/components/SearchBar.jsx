// src/pages/JobSearchPage/components/SearchBar.jsx
import React, { useState, useEffect, useRef } from 'react';
import { getSeniorities, getJobTitleSuggestions, getLocationSuggestions } from '../../../api/jobService'; // Import API service
import './SearchBar.css';

function SearchBar({ onSearch }) {
  const [searchTerm, setSearchTerm] = useState('');
  const [location, setLocation] = useState('');
  const [selectedSeniority, setSelectedSeniority] = useState('');
  const [seniorityOptions, setSeniorityOptions] = useState([]);
  const [jobTitleSuggestions, setJobTitleSuggestions] = useState([]);
  const [showJobTitleSuggestions, setShowJobTitleSuggestions] = useState(false);
  const [locationSuggestions, setLocationSuggestions] = useState([]);
  const [showLocationSuggestions, setShowLocationSuggestions] = useState(false);
  const searchContainerRef = useRef(null);
  const searchTermInputRef = useRef(null);
  const locationInputRef = useRef(null);
  const justClickedSuggestionRef = useRef(false);


  useEffect(() => {
    const fetchSeniorities = async () => {
      try {
        const seniorities = await getSeniorities();
        setSeniorityOptions(seniorities || []);
      } catch (error) {
        console.error("Error fetching seniorities:", error);
        setSeniorityOptions([]);
      }
    };
    fetchSeniorities();
  }, []);

  useEffect(() => {
    if (justClickedSuggestionRef.current) {
      justClickedSuggestionRef.current = false;
      return;
    }

    if (searchTerm.trim() === "") {
      setJobTitleSuggestions([]);
      setShowJobTitleSuggestions(false);
      return;
    }

    const timerId = setTimeout(async () => {
      try {
        const fetchedSuggestions = await getJobTitleSuggestions(searchTerm);
        setJobTitleSuggestions(fetchedSuggestions || []);
        setShowJobTitleSuggestions(fetchedSuggestions && fetchedSuggestions.length > 0);
      } catch (error) {
        console.error("Error fetching job title suggestions:", error);
        setJobTitleSuggestions([]);
        setShowJobTitleSuggestions(false);
      }
    }, 300); 

    return () => {
      clearTimeout(timerId);
    };
  }, [searchTerm]);

  useEffect(() => {
    if (justClickedSuggestionRef.current) {
          return;
    }

    if (location.trim() === "") {
      setLocationSuggestions([]);
      setShowLocationSuggestions(false);
      return;
    }

    const timerId = setTimeout(async () => {
      try {
        const fetchedSuggestions = await getLocationSuggestions(location);
        setLocationSuggestions(fetchedSuggestions || []);
        setShowLocationSuggestions(fetchedSuggestions && fetchedSuggestions.length > 0);
      } catch (error) {
        console.error("Error fetching location suggestions:", error);
        setLocationSuggestions([]);
        setShowLocationSuggestions(false);
      }
    }, 300); 

    return () => clearTimeout(timerId);
  }, [location]);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (searchContainerRef.current && !searchContainerRef.current.contains(event.target)) {
        setShowJobTitleSuggestions(false);
        setShowLocationSuggestions(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  const handleSearchClick = () => {
    setShowJobTitleSuggestions(false);
    setShowLocationSuggestions(false);
    onSearch(searchTerm, location, selectedSeniority);
  };

  const handleSearchTermChange = (e) => {
    setSearchTerm(e.target.value);
  };

  const handleLocationChange = (e) => {
    setLocation(e.target.value);
  };

  const handleJobTitleSuggestionClick = (suggestion) => {
    justClickedSuggestionRef.current = true;
    setSearchTerm(suggestion);
    setJobTitleSuggestions([]);
    setShowJobTitleSuggestions(false);
    searchTermInputRef.current?.blur(); 
  };

  const handleLocationSuggestionClick = (suggestion) => {
    justClickedSuggestionRef.current = true;
    setLocation(suggestion);
    setLocationSuggestions([]);
    setShowLocationSuggestions(false);
    locationInputRef.current?.blur(); 
  };

  return (
    <header className="search-bar" ref={searchContainerRef}>
      <div className="search-input-container">
        <input
          type="text"
          ref={searchTermInputRef} 
          placeholder="Tên công việc, vị trí bạn muốn ứng tuyển..."
          value={searchTerm}
          onChange={handleSearchTermChange}
          onFocus={() => { if (searchTerm.trim() && jobTitleSuggestions.length > 0) setShowJobTitleSuggestions(true);}}
        />
        {showJobTitleSuggestions && jobTitleSuggestions.length > 0 && (
          <ul className="suggestions-list">
            {jobTitleSuggestions.map((suggestion, index) => (
              <li key={index} onClick={() => handleJobTitleSuggestionClick(suggestion)}>
                {suggestion}
              </li>
            ))}
          </ul>
        )}
      </div>
      <div className="search-input-container">
        <input
          type="text"
          ref={locationInputRef} 
          placeholder="Địa điểm"
          value={location}
          onChange={handleLocationChange}
          onFocus={() => { if (location.trim() && locationSuggestions.length > 0) setShowLocationSuggestions(true);}}
        />
        {showLocationSuggestions && locationSuggestions.length > 0 && (
          <ul className="suggestions-list">
            {locationSuggestions.map((suggestion, index) => (
              <li key={index} onClick={() => handleLocationSuggestionClick(suggestion)}>
                {suggestion}
              </li>
            ))}
          </ul>
        )}
      </div>
      <select
        value={selectedSeniority}
        onChange={(e) => setSelectedSeniority(e.target.value)}
      >
        <option value="">Tất cả cấp bậc</option>
        {seniorityOptions.map((seniority) => (
          <option key={seniority} value={seniority || ''}>{seniority || "Chưa xác định"}</option>
        ))}
      </select>
      <button onClick={handleSearchClick}>Tìm kiếm</button>
    </header>
  );
}
export default SearchBar;