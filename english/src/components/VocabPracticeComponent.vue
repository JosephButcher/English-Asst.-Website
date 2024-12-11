<script setup>
import { ref, nextTick } from 'vue';
import axios from "axios";

const isVisible = ref(true);
const closeWindow = () => {
  isVisible.value = false;
  window.history.back();
};

const currentStep = ref(1); // 1: Word details, 2: Spelling, 3: Quiz
const wordData = ref({});
const questions = ref([]);  // Initialize questions as an empty array
const userAnswer = ref({});  // Use an object to manage answers per question
const correctWord = ref("");
const userProgress = ref({});

// Fetch word data from the server
const fetchWordData = async () => {
  try {
    const response = await axios.get("http://127.0.0.1:5000/start_new_word");
    console.log("Response Data:", response.data); // Log the response data

    if (response.data && response.data.word) {
      wordData.value = response.data;
      correctWord.value = wordData.value.word; // Ensure correctWord is assigned a valid string
      // Check if questions exist and ensure options are valid
      if (Array.isArray(wordData.value.questions)) {
        questions.value = wordData.value.questions.map((question) => {
          const options = question.options || [];  // Default to empty array if options are undefined
          return {
            ...question,
            options: shuffleOptions([question.correct_answer, ...options, "Option B", "Option C", "Option D"]),
          };
        });
      } else {
        console.error("No questions found in the response.");
      }
      userProgress.value = response.data.user_progress;
      currentStep.value = userProgress.value.current_step;
    } else {
      throw new Error("No word data found.");
    }
  } catch (error) {
    console.error("Error fetching word data:", error);
  }
};

// Shuffle answer options
const shuffleOptions = (options) => options.sort(() => Math.random() - 0.5);

// Move to the spelling step
const moveToSpellingStep = () => {
  currentStep.value = 2;
};

const userSpelling = ref(Array(correctWord.value.length).fill(''));

// In the checkSpelling method, join the array to form the word
const checkSpelling = async () => {
  try {
    const userWord = userSpelling.value.join('').toLowerCase().trim();
    const correctWordNormalized = correctWord.value.toLowerCase().trim();

    console.log("User input word:", userWord);
    console.log("Correct word:", correctWordNormalized);

    if (userWord === correctWordNormalized) {
      console.log("Spelling is correct. Checking with server...");

      // Send both user word and correct word to the server
      const response = await axios.post("http://127.0.0.1:5000/check_spelling", {
        word: userWord,
        correct_word: correctWordNormalized // Include both words
      });

      console.log("Server response:", response.data);

      if (response.data.success) {
        console.log("Spelling correct! Proceeding to step 3.");
        currentStep.value = 3;
      } else {
        alert("Incorrect spelling. Try again!");
        currentStep.value = 1;
      }
    } else {
      console.log("Spelling is incorrect.");
      alert("Incorrect spelling. Try again!");
      currentStep.value = 1;
    }
  } catch (error) {
    console.error("Error during request:", error);
    alert("Error. Try again!");
    currentStep.value = 1;
  }
};

const moveFocus = (index) => {
  nextTick(() => {
    const inputs = document.querySelectorAll(".letter-input");
    if (index < inputs.length - 1 && userSpelling.value[index]) {
      inputs[index + 1].focus();
    }
  });
};

// Initialize the word data
fetchWordData();
</script>

<template>
  <div class="overlay" v-if="isVisible">
    <div class="window">
      <div class="window-header">
        <h2>Vocabulary Practice</h2>
        <button class="exit-button" @click="closeWindow">Exit</button>
      </div>

      <!-- Word details step -->
      <div v-if="currentStep === 1" class="window-content">
        <h3 class="word">{{ wordData.word }}</h3>
        <p class="partOfSpeech">{{ wordData.part_of_speech }}</p>
        <p class="definition"><strong>Definition:</strong> {{ wordData.definition }}</p>
        <p class="example"><strong>Example:</strong> {{ wordData.example_sentence }}</p>
        <p class="synonyms"><strong>Synonyms:</strong> {{ wordData.synonyms }}</p>
        <button class="continue-button" @click="moveToSpellingStep">Continue</button>
      </div>

      <!-- Spelling step -->
      <div v-if="currentStep === 2" class="window-content">
        <h3 class="spelling-h3">How do you spell the word?</h3>
        <div class="spelling-box">
          <span v-if="correctWord" v-for="(char, index) in correctWord.split('')" :key="index">
            <input
                v-model="userSpelling[index]"
                type="text"
                maxlength="1"
                class="letter-input"
                :placeholder="char === ' ' ? ' ' : '_'"
                @input="moveFocus(index)"
            />
          </span>
        </div>
        <button class="continue-button" @click="checkSpelling">Check Spelling</button>
      </div>

      <!-- Quiz step -->
      <div v-if="currentStep === 3 && questions.length > 0" class="window-content">
        <h3 v-for="(question, index) in questions" :key="question.question_id">{{ question.text }}</h3>
        <div v-for="(option, idx) in question.options" :key="option">
          <input
              type="radio"
              :id="'option-' + index + '-' + idx"
              :value="option"
              v-model="userAnswer[question.question_id]"
          />
          <label :for="'option-' + index + '-' + idx">{{ option }}</label>
        </div>
        <button class="continue-button" @click="submitAnswer(question)">Submit Answer</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.overlay {
  position: fixed;
  height: 100%;
  width: 100%;
  top: 0;
  left: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}
.window {
  width: 65vw;
  height: 85vh;
  background: whitesmoke;
  border-radius: 15px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  overflow-y: auto;
  box-shadow: 0 6px 10px rgba(0, 0, 0, 0.3);
}
.window-header {
  display: flex;
  justify-content: space-between;
  padding: 10px;
  border-bottom: 2px solid #4A4A4A;
}
.exit-button {
  background: none;
  border: none;
  width: 8%;
  cursor: pointer;
  font-size: 2vw;
  color: #4A4A4A;
}
.exit-button:hover {
  background-color: rgba(0, 0, 0, 0.3);
}
.window-content {
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 20px 0 20px 0;
  height: 80%;
}
.spelling-h3 {
  text-align: center;
  font-size: 3vw;
  margin-bottom: 2vh;
  color: #4A4A4A;
}
.word {
  display: flex;
  justify-content: left;
  align-items: flex-start;
  font-size: 3.5rem;
  color: #007BFF;
  margin: 1vh auto 1vh 1vh;
}
.partOfSpeech, .definition, .example, .synonyms {
  font-size: 2.5vh;
  margin: 3vh auto 3vh 1vh;
  color: #4A4A4A;
}
.definition strong, .example strong, .synonyms strong {
  color: #000080;
  font-style: italic;
}
h2 {
  font-size: 4vh;
  color: #4A4A4A;
}
.continue-button {
  width: 100%;
  padding: 10px;
  margin-top: auto;
  background-color: #76c4fa;
  color: whitesmoke;
  font-size: 1.25rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}
.continue-button:hover {
  background-color: #6aa7d1;
}
.spelling-box {
  display: flex;
  gap: 5px;
  justify-content: center;
  margin-bottom: 20px;
}
.letter-input {
  width: 3rem;
  height: 3rem;
  text-align: center;
  font-size: 2rem;
  border: 1px solid #4A4A4A;
  border-radius: 5px;
}
.letter-input:disabled {
  background-color: #f0f0f0;
  color: #007BFF;
}</style>
