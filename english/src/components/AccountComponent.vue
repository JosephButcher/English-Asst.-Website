<script setup>
/* import NavBar from './NavBarComponent.vue'; */
</script>

<template>
  <body>
    <div>
      <h1>Account</h1>
    </div>
    <main>
      <div>
        <form method="post">
          <fieldset>
            <legend><h3>Account Information</h3></legend><br>
            <label for="username">First name:</label><br>
            <input type="text" id="username" name="username" placeholder="Username"><br>
            <label for="email">Email address:</label><br>
            <input type="email" id="email" name="email" placeholder="Email Address"><br>
            <label for="password">Password:</label><br>
            <input type="password" id="password" name="password" placeholder="Password"><br>

            <input type="submit" value="Submit Answers">
            </fieldset>
        </form>
      </div>
    </main>
  </body>

</template>

<style scoped>

</style>