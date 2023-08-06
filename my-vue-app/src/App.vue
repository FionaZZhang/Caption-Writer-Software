<script>
import NavBar from './components/NavBar.vue';
import Main from './components/HelloWorld.vue';
import Gallery from './components/Gallery.vue';

export default {
  components: {
    NavBar,
    Gallery,
    Main
  },
  data() {
    return {
      currentPage: 'Main',

      // Sample data for the gallery (replace with your actual data)
      galleryImages: [
        { src: './static/images/29413.png', caption: 'Image 1' },
        { src: './static/images/45332.png', caption: 'Image 2' },
        { src: './static/images/49439.png', caption: 'Image 3' },
        { src: './static/images/55051.png', caption: 'Image 4' },
        { src: './static/images/55787.png', caption: 'Image 5' },
        { src: './static/images/62084.png', caption: 'Image 6' },
        { src: './static/images/81686.png', caption: 'Image 7' },
        { src: './static/images/97000.png', caption: 'Image 8' },
        { src: './static/images/69732.png', caption: 'Image 9' },
        // Add more images and captions as needed
      ],
    };
  },
  methods: {
    switchPage(page) {
      this.currentPage = page;
    },
  },
};

</script>

<template>
  <div>
    <NavBar :currentPage="currentPage" @switchPage="switchPage" />
    <h1 style="margin-bottom: 0px;">🐈CATBox</h1>
    <Main v-if="currentPage === 'Main'" />
    <Gallery v-if="currentPage === 'Gallery'" :images="galleryImages" />
    
    <!-- <Main msg="✨AI Blog Writer" /> -->
    <!-- <Gallery :images="galleryImages" /> -->
  </div>
</template>

<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
