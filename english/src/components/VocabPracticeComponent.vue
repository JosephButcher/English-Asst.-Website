<script setup>
import { ref } from "vue";
import axios from "axios";

const isVisible = ref(true);
const closeWindow = () => {
  isVisible.value = false;
  window.history.back();
};

const currentStep = ref(1); // 1: Word details, 2: Spelling, 3: Quiz
const wordData = ref({});
const questions = ref([]);
const userSpelling = ref("");
const userAnswer = ref("");
const correctWord = ref("");
const userProgress = ref({});

const fetchWordData = async () => {
  try {
    const response = await axios.get("http://your-flask-server-url/start_new_word");
    wordData.value = response.data;
    correctWord.value = wordData.value.word;
    questions.value = wordData.value.questions.map((question) => ({
      ...question,
      options: shuffleOptions([question.correct_answer, "Option B", "Option C", "Option D"]),
    }));
    userProgress.value = response.data.user_progress;
    currentStep.value = userProgress.value.current_step;
  } catch (error) {
    console.error("Error fetching word data:", error);
  }
};

const shuffleOptions = (options) => options.sort(() => Math.random() - 0.5);

const moveToSpellingStep = () => {
  currentStep.value = 2;
};

const checkSpelling = async () => {
  try {
    const response = await axios.post("http://your-flask-server-url/check_spelling", {
      word: userSpelling.value,
      correct_word: correctWord.value,
    });
    if (response.data.correct) {
      currentStep.value = 3;
    } else {
      alert("Incorrect spelling. Try again!");
    }
  } catch {
    alert("Incorrect spelling. Try again!");
  }
};

const submitAnswer = async (question) => {
  try {
    const isCorrect = userAnswer.value === question.correct_answer;
    await axios.post("http://your-flask-server-url/update_user_progress", {
      user_id: 1,
      word_id: wordData.value.word_id,
      correct_answer: question.correct_answer,
      user_answer: userAnswer.value,
    });
    if (isCorrect) {
      const currentIndex = questions.value.indexOf(question);
      if (currentIndex === questions.value.length - 1) {
        currentStep.value = 1;
        fetchWordData();
      } else {
        userAnswer.value = "";
      }
    } else {
      alert("Incorrect answer. Try again!");
    }
  } catch (error) {
    console.error("Error submitting answer:", error);
  }
};

fetchWordData();
</script>

<template>
  <div class="overlay" v-if="isVisible">
    <div class="window">
      <div class="window-header">
        <h2>Vocabulary Practice</h2>
        <button class="exit-button" @click="closeWindow">Exit</button>
      </div>

      <div v-if="currentStep === 1" class="window-content">
        <h3 class="word">{{ wordData.word }}</h3>
        <p><strong>Definition:</strong> {{ wordData.definition }}</p>
        <p><strong>Part of Speech:</strong> {{ wordData.part_of_speech }}</p>
        <p><strong>Example Sentence:</strong> {{ wordData.example_sentence }}</p>
        <button class="continue-button" @click="moveToSpellingStep">Move On</button>
      </div>

      <div v-if="currentStep === 2" class="window-content">
        <h3>How do you spell the word?</h3>
        <input v-model="userSpelling" type="text" placeholder="Type the word here" />
        <button class="continue-button" @click="checkSpelling">Check Spelling</button>
      </div>

      <div v-if="currentStep === 3" class="window-content">
        <h3 v-for="(question, index) in questions" :key="question.question_id">{{ question.text }}</h3>
        <div v-for="option in question.options" :key="option">
          <input type="radio" :id="'option-' + index + option" :value="option" v-model="userAnswer" />
          <label :for="'option-' + index + option">{{ option }}</label>
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
.window{
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
.word {
  display: flex;
  justify-content: left;
  align-items: flex-start;
  font-size: 3.5rem;
  color: #007BFF;
  margin: 1vh auto 1vh 1vh;
}
.partOfSpeech {
  display: flex;
  justify-content: left;
  align-items: flex-start;
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
.continue-button-container {
  border-top: 2px solid #4A4A4A;
  padding-top: 10px;
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
</style>