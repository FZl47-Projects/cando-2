/*-------------START SLIDER FOR MAIN--------------*/


const swiperMain = new Swiper('#slider-main', {
  // Default parameters
  slidesPerView: 1,
  spaceBetween: 10,
  // Responsive breakpoints

  autoplay: {
      delay: 2000
  },

  pagination: {
      el: '.swiper-pagination',
      clickable: true
  },

// Navigation arrows
navigation: {
  nextEl: '.swiper-button-next',
  prevEl: '.swiper-button-prev',
},
})
/*-------------END SLIDER FOR MAIN--------------*/


const sliderHeader = new Swiper('#showcase-day-slider', {
  direction: 'horizontal',
  autoplay: {
    delay: 2000,
    loop:true,
  },
  slidesPerView:1,
  spaceBetween: 10, // <- doesn't work

 autoplay: {
     delay: 2000,
   },
   grid: {
     rows: 1,
   },

  breakpoints: {
    340: {
      slidesPerView:2,
      
    },
      600: {
        slidesPerView:2,
        spaceBetween: 10, // <- doesn't work
      },
      700: {
        slidesPerView: 3,
        spaceBetween: 10, // <- doesn't work
      },
      992: {
        slidesPerView: 4,
        spaceBetween: 10, // <- doesn't work
      },
      1200: {
          slidesPerView: 5,
          spaceBetween: 10, // <- doesn't work

        },
    },
  // If we need pagination
  pagination: {
    el: '.swiper-pagination',
    clickable: true
  },

  // Navigation arrows
  navigation: {
    nextEl: '.swiper-button-next',
    prevEl: '.swiper-button-prev',
  },

});
// ----------اسلایدر محصولات------------//


const sliderblog = new Swiper('#blog', {
  direction: 'horizontal',
  loop: true,
  
  slidesPerView:2,
  spaceBetween: 10, // <- doesn't work

 autoplay: {
     delay: 2000,
   },
   grid: {
     rows: 1,
   },

  breakpoints: {
      600: {
        slidesPerView:2,
        spaceBetween: 10, // <- doesn't work
      },
      700: {
        slidesPerView: 3,
        spaceBetween: 10, // <- doesn't work
      },
      992: {
        slidesPerView: 3,
        spaceBetween: 10, // <- doesn't work
      },
      1200: {
          slidesPerView: 4,
          spaceBetween: 15, // <- doesn't work

        },
    },
   // If we need pagination
   pagination: {
    el: '.swiper-pagination',
    clickable: true
  },

  // Navigation arrows
  navigation: {
    nextEl: '.swiper-button-next',
    prevEl: '.swiper-button-prev',
  },
});
// ----------اسلایدر محصولات------------//