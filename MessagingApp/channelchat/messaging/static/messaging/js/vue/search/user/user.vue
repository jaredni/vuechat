<template>
  <ol>
    <li v-for="todo in todos">
      {{ todo.text }}
      <!--{{ text }}-->
    </li>
  </ol>

</template>

<script>
  define(["vue"], function(Vue) {
      Vue.component("my-component", {
          template: template, // the variable template will be injected 
          //data: function() {
          //    return {"text": "Ok"};
          //}
          data: function() {
             return {"todos": [
                           { text: 'Learn JavaScript' },
                           { text: 'Learn Vue' },
                           { text: 'Build something awesome' }
                         ]}
          }

      });
    });
</script>