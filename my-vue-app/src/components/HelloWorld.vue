<script setup>
import { ref } from 'vue'

defineProps({
  msg: String,
})

const count = ref(0)
const platform = ref('') // Variable to store the selected platform
const buttons = ref({})
const generatedBlog = ref('') // the paragraph holding the generated content

// Function to handle button click and set the platform
const selectPlatform = (selectedPlatform) => {
  platform.value = selectedPlatform;
}

// Function to get the class name for the button based on the selected platform
const getButtonClass = (selectedPlatform) => {
  return platform.value === selectedPlatform ? 'focused' : ''
}


// Function to handle form submission
const submitForm = async () => {
  const userInput = document.getElementById('blog-form').value
  const postData = {
    input_text: userInput,
    style: 'formal', 
    platform: platform.value
  };

  try {
    const response = await postToBackend('http://127.0.0.1:5000/generate', postData);
    console.log(response); // Handle the response from the backend as needed
    console.log(response.output_text); // Handle the response from the backend as needed
    generatedBlog.value = response.output_text;
  } catch (error) {
    console.error(error);
  }
}

// Function to handle the post request to the backend
const postToBackend = async (url, data) => {
  console.log(data);
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    });

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return await response.json();
  } catch (error) {
    throw new Error('Error fetching data');
  }
}
</script>

<template>
  <div>
    <h1>{{ msg }}</h1>
    <div class="container">
      <div class="column left">
        <div>
          <h3 style="font-style: italic;">Choose the platform👇</h3>
          <button
            @click="selectPlatform('Instagram')"
            :class="getButtonClass('Instagram')"
            ref="buttonInsta"
          >
            Instagram
          </button>
          <p></p>
          <button
            @click="selectPlatform('YouTube')"
            :class="getButtonClass('YouTube')"
            ref="buttonYouTube"
          >
            YouTube
          </button>
          <p></p>
          <button
            @click="selectPlatform('LinkedIn')"
            :class="getButtonClass('LinkedIn')"
            ref="buttonLinkedIn"
          >
            LinkedIn
          </button>
        </div>
      </div>
      <div class="column middle">
        <textarea id="blog-form" placeholder="Enter your text here ✍️"></textarea>
        <button class="submit" @click="submitForm">Submit</button>
      </div>
      <div class="column right">
        <h3>👇Generated Blog: </h3>
        <p>{{ generatedBlog }}</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.read-the-docs {
  color: #888;
}

</style>
