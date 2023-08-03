<template>
    <div class="gallery">
        <div v-for="(image, index) in visibleImages" :key="index" class="image-container">
            <img :src="image.src" :alt="image.caption" class="image" />
            <p class="caption">{{ image.caption }}</p>
        </div>
        <!-- <p class="gap"></p> -->
    </div>
  </template>
  
  <script>
export default {
  props: {
    images: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      visibleImages: [], // Array to store the images visible in the gallery
      batchSize: 5, // Number of images to load per batch
      currentPage: 0, // Current page number
    };
  },
  created() {
    // Load initial batch of images when the component is created
    this.loadNextBatch();
    // Add an event listener to the scroll event
    window.addEventListener('scroll', this.handleScroll);
  },
  destroyed() {
    // Clean up the event listener when the component is destroyed
    window.removeEventListener('scroll', this.handleScroll);
  },
  methods: {
    loadNextBatch() {
      // Calculate the index range for the next batch of images
      const startIndex = this.currentPage * this.batchSize;
      const endIndex = startIndex + this.batchSize;

      // Add the next batch of images to the visibleImages array
      this.visibleImages = this.visibleImages.concat(this.images.slice(startIndex, endIndex));

      // Increment the current page number
      this.currentPage++;
    },
    handleScroll() {
      // Calculate the distance between the bottom of the page and the bottom of the viewport
      const distanceToBottom = document.documentElement.scrollHeight - (window.innerHeight + window.scrollY);

      // Load the next batch of images when the user is near the bottom of the page
      if (distanceToBottom < 200) {
        this.loadNextBatch();
      }
    },
  },
};
  </script>
  
  <style scoped>
  .gallery {
    display: inline-block;

  }
  
  .image-container {
    width: 200px;
  }
  
  .image {
    width: 100%;
    border-radius: 10px;
    border: 3px solid #d4aed887;
    height: auto;
  }
  
  .caption {
    text-align: center;
    margin-top: 0px;
    margin-bottom: 40px;
    background-color: #d4aed887;
    border-radius: 100px;
  }
  </style>
  