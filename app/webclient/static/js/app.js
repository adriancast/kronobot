"use strict";

var $$ = Dom7;

// App configuration
var app = new Framework7({
  root: '#app',
  theme: 'ios',
  tapHold: true,
  view: {
    stackPages: true
  },
  // Create routes for all pages
  routes: [
    {
      path: '/',
      url: 'index.html',
    },
    {
      path: '/single/',
      url: 'pages/single.html',
    },
    {
      path: '/single-2/',
      url: 'pages/single-2.html',
    },
    {
      path: '/single-elements/',
      url: 'pages/single-elements.html',
    },
    {
      path: '/author/',
      url: 'pages/author.html',
    },
    {
      path: '/cards/',
      url: 'pages/cards.html',
    },
    {
      path: '/cards-author-comments/',
      url: 'pages/cards-author-comments.html',
    },
    {
      path: '/cards-category/',
      url: 'pages/cards-category.html',
    },
    {
      path: '/cards-chip/',
      url: 'pages/cards-chip.html',
    },
    {
      path: '/cards-footer/',
      url: 'pages/cards-footer.html',
    },
    {
      path: '/cards-medium/',
      url: 'pages/cards-medium.html',
    },
    {
      path: '/cards-columns/',
      url: 'pages/cards-columns.html',
    },
    {
      path: '/list-category/',
      url: 'pages/list-category.html',
    },
    {
      path: '/list-category-author/',
      url: 'pages/list-category-author.html',
    },
    {
      path: '/list-category-date/',
      url: 'pages/list-category-date.html',
    },
    {
      path: '/slider-1/',
      url: 'pages/slider-1.html',
    },
    {
      path: '/slider-2/',
      url: 'pages/slider-2.html',
    },
    {
      path: '/slider-3/',
      url: 'pages/slider-3.html',
    },
    {
      path: '/slider-4/',
      url: 'pages/slider-4.html',
    },
    {
      path: '/categories-cards/',
      url: 'pages/categories-cards.html',
    },
    {
      path: '/categories-columns/',
      url: 'pages/categories-columns.html',
    },
    {
      path: '/category/',
      url: 'pages/category.html',
    },
    {
      path: '/author-list/',
      url: 'pages/author-list.html',
    },
    {
      path: '/contact/',
      url: 'pages/contact.html',
    },
    {
      path: '/pull-to-refresh/',
      url: 'pages/pull-to-refresh.html',
    },
    {
      path: '/infinite-scroll/',
      url: 'pages/infinite-scroll.html',
    },
    {
      path: '/promo-banner/',
      url: 'pages/promo-banner.html',
    }
  ]
});



// Function to scale cards when pushed
function activeCardTouch() {
  $$('.card').on('touchstart', function(e){
    $$(this).addClass('card-scale');
  });
  $$('.card').on('touchend', function(e){
    $$(this).removeClass('card-scale');
  });

  $$('.card').on('mousedown', function(){
    $$(this).addClass('card-scale');
  });
  $$('.card').on('mouseup', function(){
    $$(this).removeClass('card-scale');
  });

  $$('.swiper-slide a').on('click', function(e){
    window.location.href = $$(this).attr('href');
  });
}

// Load the fonction on app init
activeCardTouch();

// Load the function on new elements when a page is opened
app.on('pageInit', function(page) {
  activeCardTouch();
});


// Create searchbar
var searchbar = app.searchbar.create({
  el: '.searchbar',
  searchContainer: '.list',
  searchIn: '.item-title',
  customSearch: true,
  on: {
    search(sb, query) {
      if(query == ''){
        $$('.search-results').hide();
      }
      else{
        $$('.search-preloader').show();
        // Emulate 0.5s loading for the demo
        // You can do an Ajax request here
        setTimeout(function () {
          $$('.search-preloader').hide();
          $$('.search-results').show();
        }, 500);
      }
    },
    clear(sb, previousQuery) {
      $$('.search-results').hide();
    },
    disable(sb) {
      $$('.search-results').hide();
    }
  }
});

// Automatically fill in the search field when you click on a suggestion
$$('.page-search .popular-tags li').on('click', function(e){
  searchbar.search($$(this).find('span').text());
})
$$('.page-search .trending-search ul li').on('click', function(e){
  searchbar.search($$(this).find('.item-title a').text());
})



// Common options to all sliders
var swiperOptions = {
  spaceBetween: 10,
  touchMoveStopPropagation: false,
  on: {
    touchStart: function(e){
      $$(e.target.closest('.card')).addClass('card-scale');
    },
    touchEnd: function(e){
      $$(e.target.closest('.card')).removeClass('card-scale');
    }
  }
};


// Create the Discover tab sliders
var discoverSwiper = new Swiper ('#discover-swiper', Object.assign({}, swiperOptions, {width: 320}));
var discoverSwiper2 = new Swiper ('#discover-swiper2', Object.assign({}, swiperOptions, {width: 360}));
var discoverSwiper3 = new Swiper ('#discover-swiper3', Object.assign({}, swiperOptions, {width: 360}));
var discoverSwiper5 = new Swiper ('#discover-swiper4', Object.assign({}, swiperOptions, {width: 360}));
var discoverSwiper5 = new Swiper ('#discover-swiper5', Object.assign({}, swiperOptions, {width: 360}));


// Create the Related Posts slider on Single pages
$$(document).on('page:init', '.page[data-name="single"]', function (e) {
  var rpSwiper = new Swiper (e.detail.$el.find('.single-swiper'), Object.assign({}, swiperOptions, {width: 280}));
});


// Pull to refresh on Today tab
$$('.ptr-content').on('ptr:refresh', function (e) {
  // Emulate 1s loading
  // You can do an Ajax request here to retrieve your posts from a database
  setTimeout(function () {
    var html =
    '<div class="title-container">'+
      '<span class="title-date">Tuesday 19 March</span>'+
      '<h1>Just Now</h1>'+
    '</div>'+
    '<a href="/single/">'+
      '<div class="card">'+
        '<img class="card-image" src="img/thumb-14.jpg" alt="">'+
        '<div class="card-infos">'+
          '<h2 class="card-title">How to Get Your First Tattoo Right</h2>'+
          '<div class="card-bottom">'+
            '<div class="card-author">'+
              '<img class="card-author-image" src="img/authors/author-1.jpg" alt="">'+
              '<div>Camille Aline</div>'+
            '</div>'+
            '<div class="card-comments"><i class="f7-icons">chat_bubble_fill</i></i>3</div>'+
          '</div>'+
        '</div>'+
      '</div>'+
    '</a>';

    // Prepend new list element
    $$('.ptr-content').find('#today-content').prepend(html);
    // Active cards animation to the new elements
    activeCardTouch();
    // When loading done, we reset it
    app.ptr.done();
  }, 1000);
});


// Infinite scroll on Today tab
var allowInfinite = true;

$$('.infinite-scroll-content').on('infinite', function () {
  // Exit, if loading in progress
  if (!allowInfinite) return;
  allowInfinite = false;

  // Emulate 1s loading
  // (You can do an Ajax request here to retrieve your next posts)
  setTimeout(function () {
    allowInfinite = true;

    // Generate new items HTML for the demo
    var html =
    '<li>'+
      '<a href="/single/">'+
        '<div class="item-content">'+
          '<div class="item-media"><img src="img/thumb-15.jpg" width="44"/></div>'+
          '<div class="item-inner">'+
            '<div class="item-subtitle">Fashion</div>'+
            '<div class="item-title">Archery at the 2024 Olympic Games</div>'+
            '<div class="item-subtitle bottom-subtitle"><img src="img/authors/author-3.jpg">Jess Roxana</div>'+
          '</div>'+
        '</div>'+
      '</a>'+
    '</li>'+
    '<li>'+
      '<a href="/single/">'+
        '<div class="item-content">'+
          '<div class="item-media"><img src="img/thumb-16.jpg" width="44"/></div>'+
          '<div class="item-inner">'+
            '<div class="item-subtitle">Fashion</div>'+
            '<div class="item-title">Most Beautiful Beach of the Costa Brava</div>'+
            '<div class="item-subtitle bottom-subtitle"><img src="img/authors/author-2.jpg">Zorka Ivka</div>'+
          '</div>'+
        '</div>'+
      '</a>'+
    '</li>';

    // Append new items
    $$('#infinite-content').append(html);

    // Nothing more to load, detach infinite scroll events to prevent unnecessary loadings
    app.infiniteScroll.destroy('.infinite-scroll-content');

    // Remove preloader
    $$('.infinite-scroll-preloader').remove();
  }, 1000);
});