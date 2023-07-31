<script setup>
import { ref, onMounted } from 'vue'

defineProps({
  msg: String,
})

const platform = ref('') // Variable to store the selected platform
const style = ref('') // Variable to store the selected style
const generatedBlog = ref('') // the paragraph holding the generated content
const imageFiles = ref([]) 
const imagePreview = ref(null) // Variable to store the URL for image preview

// Function to handle button click and set the platform
const selectPlatform = (selectedPlatform) => {
  platform.value = selectedPlatform;
}

const selectStyle = (selectedStyle) => {
  style.value = selectedStyle;
}

// Function to get the class name for the button based on the selected platform
const getButtonClassPlatform = (selectedPlatform) => {
  return platform.value === selectedPlatform ? 'focused' : ''
}

const getButtonClassStyle = (selectedStyle) => {
  return style.value === selectedStyle ? 'focused' : ''
}

// Function to handle form submission
const submitForm = async () => {
  const editableDiv = document.getElementById('blog-form');
  const userInput = editableDiv.textContent;
  // const postData = {
  //   input_text: userInput,
  //   file: imageFile.value
  //   // style: style.value, 
  //   // platform: platform.value
  // };
  const postData = new FormData();
  postData.append('file', imageFiles.value);
  postData.append('user_input', userInput);

  try {
    const response = await postToBackend('http://127.0.0.1:5000/generate', postData);
    console.log(response); // Handle the response from the backend as needed
    console.log(response.output_text); // Handle the response from the backend as needed
    generatedBlog.value = response.caption;
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
      // headers: {
      //   'Content-Type': 'application/json'
      // },
      // body: JSON.stringify(data)
      body: data
    });

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return await response.json();
  } catch (error) {
    throw new Error('Error fetching data');
  }
}

// Function to handle image upload and show preview
const handleImageUpload = (event) => {
  const files = event.target.files;
  if (files.length <= 9) {
    // Create an array of image files and store it in the imageFiles ref
    imageFiles.value = Array.from(files);
  } else {
    // Display an error message or take appropriate action for exceeding the file limit
    console.error('You can only upload up to 9 images.');
  }

  // const file = event.target.files[0];
  imageFiles.value = files;
  console.log(files);

  // Create a URL for image preview
  // imagePreview.value = URL.createObjectURL(files);
}
// Function to handle the initial setup of the editable div
const setupEditableDiv = () => {
  const editableDiv = document.getElementById('blog-form');
  editableDiv.innerHTML = 'Enter your text here ✍️';
}

// Function to handle when the editable div gains focus
const handleFocus = () => {
  const editableDiv = document.getElementById('blog-form');
  if (editableDiv.textContent.trim() === 'Enter your text here ✍️') {
    editableDiv.innerHTML = ''; // Remove the placeholder text when the div gains focus
  }
}

// Function to handle when the editable div loses focus
const handleBlur = () => {
  const editableDiv = document.getElementById('blog-form');
  if (editableDiv.textContent.trim() === '') {
    editableDiv.innerHTML = 'Enter your text here ✍️'; // Add back the placeholder text if the div is empty
  }
}

// Function to create the object URL for a given file
const createObjectURL = (file) => {
  return URL.createObjectURL(file);
};

// Call the setupEditableDiv function when the component is mounted
onMounted(setupEditableDiv);

</script>

<template>
    <div class="container">
      <div class="column left">
        <div>
          <h3 style="font-style: italic;">Choose the platform👇</h3>
          <button
            @click="selectPlatform('Instagram')"
            :class="getButtonClassPlatform('Instagram')"
            ref="buttonInsta"
          >
            Instagram
          </button>
          <p></p>
          <button
            @click="selectPlatform('YouTube')"
            :class="getButtonClassPlatform('YouTube')"
            ref="buttonYouTube"
          >
            YouTube
          </button>
          <p></p>
          <button
            @click="selectPlatform('LinkedIn')"
            :class="getButtonClassPlatform('LinkedIn')"
            ref="buttonLinkedIn"
          >
            LinkedIn
          </button>
        </div>
        <div>
          <h3 style="font-style: italic;">Choose the style👇</h3>
          <button
            @click="selectStyle('Informal')"
            :class="getButtonClassStyle('Informal')"
            ref="buttonInformal"
          >
            Informal
          </button>
          <p></p>
          <button
            @click="selectStyle('Formal')"
            :class="getButtonClassStyle('Formal')"
            ref="buttonFormal"
          >
            Formal
          </button>
        </div>
      </div>
      <div class="column middle">
        <!-- <textarea id="blog-form" placeholder="Enter your text here ✍️"></textarea> -->
        <!-- <textarea id="blog-form" placeholder="Enter your text here ✍️">
          {{ imageFile ? '![Uploaded Image](' + URL.createObjectURL(imageFile) + ')' : '' }}
        </textarea>
        <input type="file" accept="image/*" @change="handleImageUpload">
        <button class="submit" @click="submitForm">Submit</button> -->
        <div
          id="blog-form"
          class="editable-div"
          contenteditable
          @input="handleContentChange"
          @paste="handlePaste"
          @focus="handleFocus"
          @blur="handleBlur"
        ></div>
        <!-- <input type="file" accept="image/*" @change="handleImageUpload"> -->
        <!-- <div v-if="imagePreview">
          <img :src="imagePreview" alt="Image Preview">
        </div> -->
        <!-- <div class="image-upload">
          <label for="file-input" class="image-upload-label">
            <img v-if="imagePreview" :src="imagePreview" alt="Uploaded Image" class="image-preview">
            <div v-else class="placeholder">Upload Image</div>
          </label>
          <input id="file-input" type="file" accept="image/*" @change="handleImageUpload" multiple>
        </div> -->
        <div class="image-upload">
          <label for="file-input" class="image-upload-label">
            <!-- Display the uploaded images in a grid or other arrangement -->
            <!-- <div v-for="(file, index) in imageFiles" :key="index" class="image-preview">
              <img :src="URL.createObjectURL(file)" alt="Uploaded Image">
            </div> -->
            <img width="100" height="100" v-for="file in imageFiles" :key="file.name" :src="createObjectURL(file)" alt="Uploaded Image">
            <!-- Show the "Upload Image" placeholder only if there are no images -->
            <div v-if="imageFiles.length === 0" class="placeholder">
              <span>Upload Image</span>
            </div>
          </label>
          <input id="file-input" type="file" accept="image/*" @change="handleImageUpload" multiple>
        </div>
        <div class="submit-cell">
          <button class="submit" @click="submitForm">Submit</button>
        </div>
        <!-- Display the image preview -->
        
      </div>
      <div class="column right">
        <h3>👇Generated Blog: </h3>
        <p>{{ generatedBlog }}</p>
      </div>
    </div>
</template>

<style scoped>


</style>
