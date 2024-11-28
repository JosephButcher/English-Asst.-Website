<script setup>
</script>


<template>
  <header>
    <nav class="container">
      <ul class="nav">
        <li class="left-item"><router-link to="/">JoJiMa</router-link></li>

          <li class="middle-items"><router-link to="/RootsComponent">Latin/Greek Roots</router-link></li>
          <li class="middle-items"><router-link to="/VocabularyComponent">Vocabulary</router-link></li>
          <li class="middle-items"><router-link to="/FiguresOfSpeechComponent">Figures of Speech</router-link></li>
          <li class="middle-items"><router-link to="/ConfusingWordsComponent">Confusing Words</router-link></li>

        <li class="right-item"><router-link to="/AccountComponent">Account</router-link></li>
      </ul>
    </nav>
  </header>
</template>


<style scoped>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}
header {
  display: flex;
}
.container {
  top: 0;
  display: flex;
  justify-content: center;
  height: 5vh;
  width: 100vw;
  padding: 1rem;
  margin-bottom: 1%;
  background: #76c4fa;
}
.nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  list-style-type: none;
  width: 100%;
  padding: 0 1.5em 0;
  margin: 0;
}
.middle-items, .left-item, .right-item {
  flex: 1;
}
.middle-items {
  display: flex;
  justify-content: space-evenly;
  margin: 0 0.5rem;
}
.middle-items li {
  padding: 0 0.5rem;
}
.nav a {
  text-decoration: none;
  color: whitesmoke;
  font-weight: 750;
}
.nav a:hover {
  text-decoration: underline;
}
.nav li a {
  display: block;
  padding: 0.5rem 1rem;
  text-align: center;
  text-decoration: none;
  font-weight: 750;
}
</style>