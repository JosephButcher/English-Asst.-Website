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
            <legend>Account Information</legend>
            <label for="fname">First name:</label><br>
            <input type="text" id="fname" name="fname" placeholder="First Name">
            <label for="lname">Last name:</label><br>
            <input type="text" id="lname" name="lname" placeholder="Last Name">
            <label for="email">Email address:</label><br>
            <input type="email" id="email" name="email" placeholder="Email Address">
            <label for="password">Password:</label><br>
            <input type="password" id="password" name="password" placeholder="Password">

            <input type="submit" value="Submit Answers">
            </fieldset>
        </form>
      </div>
    </main>
  </body>

</template>

<style scoped>

</style>