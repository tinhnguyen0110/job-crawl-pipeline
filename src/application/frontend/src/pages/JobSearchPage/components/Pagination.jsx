import React from 'react';
import '../../../assets/styles/pagination.css'; // Adjust the path as necessary

function Pagination({ currentPage, totalPages, onPageChange }) {
  const getVisiblePageNumbers = () => {
    const pages = [];
    
    // Calculate start and end page numbers to show
    let startPage = Math.max(currentPage - 1, 1);
    let endPage = Math.min(startPage + 2, totalPages);
    
    // Adjust startPage if we're near the end
    if (endPage === totalPages) {
      startPage = Math.max(endPage - 2, 1);
    }

    // Generate array of visible page numbers
    for (let i = startPage; i <= endPage; i++) {
      pages.push(i);
    }

    return pages;
  };

  return (
    <nav className="pagination">
      <button 
        className="pagination-btn"
        onClick={() => onPageChange(currentPage - 1)}
        disabled={currentPage === 1}
      >
        Previous
      </button>

      {getVisiblePageNumbers().map((number) => (
        <button
          key={number}
          className={`pagination-btn ${currentPage === number ? 'active' : ''}`}
          onClick={() => onPageChange(number)}
        >
          {number}
        </button>
      ))}

      <button
        className="pagination-btn"
        onClick={() => onPageChange(currentPage + 1)}
        disabled={currentPage === totalPages}
      >
        Next
      </button>
    </nav>
  );
}

export default Pagination;