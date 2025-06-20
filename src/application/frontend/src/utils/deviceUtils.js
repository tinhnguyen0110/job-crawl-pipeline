/**
 * Kiểm tra xem screen width có phải mobile breakpoint không
 * @returns {boolean} true nếu screen width <= 767px
 */
export const isMobileBreakpoint = () => {
  return window.innerWidth <= 767;
};
