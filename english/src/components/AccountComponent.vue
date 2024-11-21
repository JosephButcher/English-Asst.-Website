<script setup>
  /* import NavBar from './NavBarComponent.vue'; */
</script>

<template>
  <body>
    <h1>Account</h1>
    <div>
      <form method="post" class="container">
        <fieldset>
          <input type="text" name="name" placeholder="Name" required><br>
          <input type="email" name="email" placeholder="Email" required><br>
          <input type="password" name="password" placeholder="Password" required><br>
          <input type="submit" value="Change Information">
        </fieldset>
      </form>
    </div>
  </body>
</template>

<style scoped>
* {
  margin: 0;
  padding: 0;
}
html {
  height: 100%;
}
body {
  display: flex;
  flex-direction: column;
  height: 100vh;
  width: 100vw;
  background-color: #3C3C3C;
}
div {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  width: 80%;
}
fieldset {
  width: 100%;
  background-color: #F3F3F3;
}
</style>