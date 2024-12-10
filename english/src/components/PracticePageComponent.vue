<template>
  <div>
    <div v-if="currentStep === 1">
      <h2>{{ wordData.word }}</h2>
      <p><strong>Definition:</strong> {{ wordData.definition }}</p>
      <p><strong>Part of Speech:</strong> {{ wordData.part_of_speech }}</p>
      <p><strong>Synonyms:</strong> {{ wordData.synonyms }}</p>
      <p><strong>Example Sentence:</strong> {{ wordData.example_sentence }}</p>
      <button @click="moveToSpellingStep">Move On</button>
    </div>

    <div v-if="currentStep === 2">
      <h2>How do you spell the word?</h2>
      <input v-model="userSpelling" type="text" placeholder="Type the word here" />
      <button @click="checkSpelling">Check Spelling</button>
    </div>

    <div v-if="currentStep === 3" v-for="(question, index) in questions" :key="question.question_id">
      <h3>{{ question.text }}</h3>
      <div v-for="option in question.options" :key="option">
        <input type="radio" :id="'option-' + index + option" :value="option" v-model="userAnswer" />
        <label :for="'option-' + index + option">{{ option }}</label>
      </div>
      <button @click="submitAnswer(question)">Submit Answer</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      wordData: {},
      questions: [],
      currentStep: 1, // Step 1: Show word details, Step 2: Spelling check, Step 3: Multiple choice
      userSpelling: '',
      userAnswer: '',
      correctWord: '',
      userProgress: {}
    };
  },
  mounted() {
    this.fetchWordData();
  },
  methods: {
    async fetchWordData() {
      try {
        const response = await axios.get('http://your-flask-server-url/start_new_word');
        this.wordData = response.data;
        this.correctWord = this.wordData.word;  // Store the correct word for spelling check
        this.questions = this.wordData.questions.map((question) => ({
          ...question,
          options: this.shuffleOptions([question.correct_answer, 'Option B', 'Option C', 'Option D']),
        }));
        this.userProgress = response.data.user_progress;  // Set initial user progress
        this.currentStep = this.userProgress.current_step;  // Get the current step from progress
      } catch (error) {
        console.error('Error fetching word data:', error);
      }
    },

    shuffleOptions(options) {
      return options.sort(() => Math.random() - 0.5); // Shuffle the answer options
    },

    moveToSpellingStep() {
      this.currentStep = 2;
    },

    async checkSpelling() {
      try {
        const response = await axios.post('http://your-flask-server-url/check_spelling', {
          word: this.userSpelling,
          correct_word: this.correctWord,
        });

        if (response.data.correct) {
          this.currentStep = 3; // Move to multiple-choice questions
        } else {
          alert('Incorrect spelling. Try again!');
        }
      } catch (error) {
        alert('Incorrect spelling. Try again!');
      }
    },

    async submitAnswer(question) {
      try {
        const isCorrect = this.userAnswer === question.correct_answer;
        await axios.post('http://your-flask-server-url/update_user_progress', {
          user_id: 1, // Assuming user ID is available
          word_id: this.wordData.word_id,
          correct_answer: question.correct_answer,
          user_answer: this.userAnswer
        });

        if (isCorrect) {
          if (this.questions.indexOf(question) === this.questions.length - 1) {
            // End of the quiz, show a new word
            this.currentStep = 1; // Go back to the starting definitions page
            this.fetchWordData();
          } else {
            // Move to the next question
            this.userAnswer = ''; // Reset the answer
            this.currentStep = 3; // Go to next question
          }
        } else {
          // Incorrect answer, stay on the same question
          alert('Incorrect answer. Try again!');
        }
      } catch (error) {
        console.error('Error submitting answer:', error);
      }
    }
  }
};
</script>