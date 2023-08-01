<script setup>
import { ref, onMounted } from 'vue'

defineProps({
  msg: String,
})

const platform = ref('') // Variable to store the selected platform
const language = ref('') // Variable to store the selected style
const generatedBlog = ref(null) // the paragraph holding the generated content
const imageFiles = ref([]) 
const loading = ref(false); // Variable to control loading message visibility
const caption = ref('');  // Variable for user input caption
const requirements = ref(''); // Variable for additional requirements


// Function to handle button click and set the platform
const selectPlatform = (selectedPlatform) => {
  platform.value = selectedPlatform;
}

const selectLanguage = (selected) => {
  language.value = selected;
}

// Function to get the class name for the button based on the selected platform
const getButtonClassPlatform = (selectedPlatform) => {
  return platform.value === selectedPlatform ? 'focused' : ''
}

const getButtonClassLanguage = (selected) => {
  return language.value === selected ? 'focused' : ''
}

// Function to handle form submission
const submitForm = async () => {
  // Reset the generatedBlog ref to null before making the API call
  generatedBlog.value = null;

  // const editableDiv = document.getElementById('blog-form');
  // const userInput = editableDiv.textContent;
  // const postData = {
  //   input_text: userInput,
  //   file: imageFile.value
  //   // style: style.value,
  //   // platform: platform.value
  // };

  // check if the input text is empty
  // if (userInput.trim() === '') {
  //   alert('Please enter some text');
  //   return;
  // }

  // check if the platform is empty
  if (platform.value === '') {
    alert('Please select a platform');
    return;
  }

  // check if the style is empty
  if (language.value === '') {
    alert('Please select a language');
    return;
  }

  // check if the image file is empty
  if (imageFiles.value.length === 0) {
    alert('Please upload an image');
    return;
  }

  // const postData = {
  //   input_text: userInput,
  //   file: imageFile.value
  //   // style: style.value,
  //   // platform: platform.value
  // };
  const postData = new FormData();
  for (const file of imageFiles.value){
    console.log(file);
    postData.append('files', file);
  }
  // console.log(userInput)
  console.log('requirements', requirements.value)
  console.log('caption', caption.value)
  // postData.append('user_input', userInput);
  postData.append('language', language.value);
  postData.append("platform", platform.value);
  postData.append('requirements', requirements.value);
  postData.append('caption', caption.value);

  // const loadingPlaceholder = document.getElementById('loading-placeholder');
  // loadingPlaceholder.textContent = 'Generating...';

  // Show the loading message
  loading.value = true;


  try {
    const response = await postToBackend('http://127.0.0.1:5000/generate', postData);
    console.log(response); // Handle the response from the backend as needed
    const outputArray = splitStringIntoParts(response.caption);
    // const testResponse = "1. A quote from a book/movie/celebrity, cite where it comes from; 2. Using only emojis; 3. An interesting word or sentence in an European language except English and Chinese, include a translation; 4. A caption that you think is appropriate. Here are the tags describing the pictures, get the vibe not the actual words: lab coat, potter's wheel, pajamas, vestment, stethoscope, silver, website, menu, envelope, crossword, plow, white. ";
    // const outputArray = splitStringIntoParts(testResponse);
    console.log(outputArray);
    generatedBlog.value = outputArray;
  } catch (error) {
    console.error(error);
  } finally {
    // Hide the loading message
    loading.value = false;
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
      body: data,
      mode: 'cors'
    });

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return await response.json();
  } catch (error) {
    // TODO: push a warning message to the user
    throw new Error('Error fetching data');
  }
}

// Function to regenerate a specific caption based on its index
const regenerateCaption = async (index) => {
  console.log(index)
  // Only regenerate if there are already generated captions
  if (generatedBlog.value) {
    try {
      const postData = new FormData();
      postData.append('caption-index', index + 1);

      // Show the loading message
      //TODO: only show loading at the disappearing button
      loading.value = true;

      const response = await postToBackend('http://127.0.0.1:5000/regenerate', postData);
      const outputArray = splitStringIntoParts(response.caption);
      
      // Replace the regenerated caption
      generatedBlog.value[index] = outputArray;
      
      // Hide the loading message
      loading.value = false;
    } catch (error) {
      console.error(error);
    }
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
// Function to handle the initial setup of the editable caption
const setupEditableCap = () => {
  const editableCap = document.getElementById('caption-input');
  editableCap.innerHTML = '(optional) enter your captions here ✍️';
}

// Function to handle when the editable caption gains focus
const handleFocusCap = () => {
  const editableCap = document.getElementById('caption-input');
  if (editableCap.textContent.trim() === '(optional) enter your captions here ✍️') {
    editableCap.innerHTML = ''; // Remove the placeholder text when the div gains focus
  }
}

// Function to handle when the editable caption loses focus
const handleBlurCap = () => {
  const editableDiv = document.getElementById('caption-input');
  if (editableDiv.textContent.trim() === '') {
    editableDiv.innerHTML = '(optional) enter your captions here ✍️'; // Add back the placeholder text if the div is empty
  }
}

const handleContentChangeCap = () => {
  const editableCap = document.getElementById('caption-input');
  caption.value = editableCap.textContent;
}

const handleContentChangeReq = () => {
  const editableReq = document.getElementById('requirements-input');
  requirements.value = editableReq.textContent;
}

// Function to handle the initial setup of the editable requirements
const setupEditableReq = () => {
  const editableReq = document.getElementById('requirements-input');
  editableReq.innerHTML = "(optional) your requirements, eg. 'I want positive/moody captions...'";
}

// Function to handle when the editable caption gains focus
const handleFocusReq = () => {
  const editableReq = document.getElementById('requirements-input');
  if (editableReq.textContent.trim() === "(optional) your requirements, eg. 'I want positive/moody captions...'") {
    editableReq.innerHTML = ''; // Remove the placeholder text when the div gains focus
  }
}

// Function to handle when the editable caption loses focus
const handleBlurReq = () => {
  const editableDiv = document.getElementById('requirements-input');
  if (editableDiv.textContent.trim() === '') {
    editableDiv.innerHTML = "(optional) your requirements, eg. 'I want positive/moody captions...'"; // Add back the placeholder text if the div is empty
  }
}
// Function to create the object URL for a given file
const createObjectURL = (file) => {
  return URL.createObjectURL(file);
};

function splitStringIntoParts(inputString) {
  const regex = /\d+\.\s/; // Regular expression to match a number followed by a dot and a space
  let parts = inputString.split(regex);
  parts = parts.slice(1, parts.length)
  console.log(parts);
  return parts;
}


// Call the setupEditable function when the component is mounted
onMounted(() => {
  setupEditableCap();
  setupEditableReq();
});

</script>

<template>
    <div class="container">
      <div class="row1">
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
            @click="selectPlatform('WeChat')"
            :class="getButtonClassPlatform('WeChat')"
            ref="buttonWeChat"
          >
            WeChat
          </button>
        </div>
        <div>
          <h3 style="font-style: italic;">Choose the language👇</h3>
          <button
            @click="selectLanguage('English')"
            :class="getButtonClassLanguage('English')"
            ref="buttonEnglish"
          >
            English
          </button>
          <p></p>
          <button
            @click="selectLanguage('Chinese')"
            :class="getButtonClassLanguage('Chinese')"
            ref="buttonChinese"
          >
            Chinese
          </button>
        </div>
      </div>
      <div class="column middle">
        <div
          id="caption-input"
          class="editable-caption"
          contenteditable
          @input="handleContentChangeCap"
          @paste="handlePaste"
          @focus="handleFocusCap"
          @blur="handleBlurCap"
        >
        </div>
        <br>
        <div
          id="requirements-input"
          class="editable-requirements"
          contenteditable
          @input="handleContentChangeReq"
          @paste="handlePaste"
          @focus="handleFocusReq"
          @blur="handleBlurReq"
        >
      </div>
      <br>
        <!-- <textarea id="blog-form" placeholder="Enter your text here ✍️"></textarea> -->
        <!-- <textarea id="blog-form" placeholder="Enter your text here ✍️">
          {{ imageFile ? '![Uploaded Image](' + URL.createObjectURL(imageFile) + ')' : '' }}
        </textarea>
        <input type="file" accept="image/*" @change="handleImageUpload">
        <button class="submit" @click="submitForm">Submit</button> -->
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
    </div>
    <p></p>
    <div class="row2">
        <h3>👇AI Generated Blog: </h3>
        <div v-if="generatedBlog">
          <button class="generated-blog-button" v-for="(output, index) in generatedBlog" :key="index" @click="regenerateCaption(index)">{{ output }}</button>
        </div>
        <div v-else>
          <p id="loading-placeholder" v-if="loading">Loading...</p>
        </div>
      </div>
    </div>
</template>

<style scoped>


</style>