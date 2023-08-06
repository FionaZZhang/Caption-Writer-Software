<template>
    <nav>
      <ul>
        <li @click="switchPage('Main')">Main</li>
        <li @click="switchPage('Gallery')">Gallery</li>
      </ul>
    </nav>
  </template>
  
  <script>
  export default {
    methods: {
      switchPage(page) {
        this.$emit('switch-page', page);
      },
    },
  };
  </script>
  
  <style scoped>
  nav {
    /* background-color: white; */
    color: #d372df;
    padding: 10px;
  }
  
  ul {
    padding-inline-start: 0;
    list-style: none;
    display: flex;
    justify-content: space-around;
    font-family: cursive;
    font-size: x-large;
    border-bottom: 3px solid;
  }
  
  li {
    margin: 0 10px;
    cursor: pointer;
  }
  </style>
  