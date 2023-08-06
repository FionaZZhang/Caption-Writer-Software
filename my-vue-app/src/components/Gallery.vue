<template>
    <div class="gallery">
      <div class="image-col-left">
        <div v-for="(image, index) in visibleImages" :key="index" class="image-container">
            <img :src="image.src" class="image-left" />
            <!-- <p class="caption">{{ image.caption }}</p> -->
        </div>
      </div>
      <div class="image-col-middle">
        <div v-for="(image, index) in visibleImages" :key="index" class="image-container">
            <img :src="image.src" class="image-middle" />
            <!-- <p class="caption">{{ image.caption }}</p> -->
        </div>
      </div>
      <div class="image-col-right">
        <div v-for="(image, index) in visibleImages" :key="index" class="image-container">
            <img :src="image.src" class="image-right" />
            <!-- <p class="caption">{{ image.caption }}</p> -->
        </div>
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
    overflow: hidden;
    border: 3px solid #d4aed887;
    border-radius: 10px;
    max-height: 500px;
    max-width: 800px;
    width: -webkit-fill-available;
    height: -webkit-fill-available;
  }
  
  .image-container {
    /* width: 200px;
    display: block; */
  }
  
  .image-left {
    width: 100%;
    border-radius: 10px;
    border: 3px solid #d4aed887;
    height: auto;
    transform: translateY(100vh);
    animation: float-up-2 12s linear infinite;
    z-index: 1;
  }
  .image-middle {
    width: 100%;
    border-radius: 10px;
    border: 3px solid #d4aed887;
    height: auto;
    transform: translateY(100vh);
    animation: float-up-1 10s linear infinite;
    z-index: 1;
  }

  .image-right {
    width: 100%;
    border-radius: 10px;
    border: 3px solid #d4aed887;
    height: auto;
    transform: translateY(100vh);
    animation: float-up-3 12s linear infinite;
    z-index: 1;
  }
  
  .caption {
    text-align: center;
    margin-top: 0px;
    margin-bottom: 40px;
    background-color: #d4aed887;
    border-radius: 100px;
  }

/* @mixin setImage($a, $x) {
  --name: float-up-#{$a};
  --duration: calc(20s * #{$a});
  left: #{$x}vw;
  z-index: -1 * $a;
}

img {
  --duration: 40s;
  --name: float-up-1;
  position: absolute;
  top: 0;
  left: 0;
  width: 33vw;
  transform: translateY(200vh);
  animation: var(--name) var(--duration) linear infinite;
  box-shadow: 1px 3px 15px rgba(0,0,0,0.5);
  z-index: 1;

  @for $i from 1 through 10 {
    &:nth-child(#{$i}) {
      animation-delay: ($i - 1) * -3s;
    }
  }
  
  &:nth-child(1)  { @include setImage(1,  0) }
  &:nth-child(2)  { @include setImage(3, 10) }
  &:nth-child(3)  { @include setImage(2, 90) }
  &:nth-child(4)  { @include setImage(1, 36) }
  &:nth-child(5)  { @include setImage(3, 62) }
  &:nth-child(6)  { @include setImage(2, 15) }
  &:nth-child(7)  { @include setImage(2, 55) }
  &:nth-child(8)  { @include setImage(3,-20) }
  &:nth-child(9)  { @include setImage(1, 68) }
  &:nth-child(10) { @include setImage(2,  0) }
} */

@keyframes float-up-3 {
  from {
    transform: translateY(100vh) translateZ(-50vh);
  }
  to {
    transform: translateY(-150vh) translateZ(-50vh);
  }
}

@keyframes float-up-2 {
  from {
    transform: translateY(80vh) translateZ(-25vh);
  }
  to {
    transform: translateY(-150vh) translateZ(-25vh);
  }
}

@keyframes float-up-1 {
  from {
    transform: translateY(50vh);
  }
  to {
    transform: translateY(-150vh);
  }
}

.image-col-left {
  width: 200px;
  display: inline-block;
}
.image-col-middle {
  width: 200px;
  display: inline-block;
}
.image-col-right {
  width: 200px;
  display: inline-block;
}

  </style>
  