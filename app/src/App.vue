<template>
        <div id="app">
            <router-view/>
        </div>
       <!-- <v-app id="app" standalone>
        <v-toolbar fixed>
             <v-container>
            <v-toolbar-title class="orange--text text-xs-center">JARIS</v-toolbar-title>
            </v-container>
        </v-toolbar>
        <main>
            <v-container>
               <router-view></router-view>
            </v-container>
        </main>
    </v-app> -->
</template>

<script>
export default {
    name: 'app',
    // provide (){
    //     return {
    //         reload: this.reload
    //     }
    // },
    // data () {
    // return {
    //     isRouterAlive: true
    // }
    // },
    // methods: {
    // reload () {
    //     this.isRouterAlive = false
    //     this.$nextTick(() => (this.isRouterAlive = true))
    // }   
    // }

}
</script>

<style>
#app {
  margin-top: 60px;
}
.ctrl {
  margin-bottom: 1.6rem;  
}
.card-text {
    white-space: pre-wrap;

  }
.header {
  color: #555;
  height: 100%;
  text-align: center;
  padding-top: 5px;
}
.header .cover-heading {
  /* font-family: sans-serif, serif; */
  font-size: 70px;
  color: #3e34f9;
  margin-top: 3.6rem;
  margin-bottom: 0.5rem;
}
.card {
  text-align: left;
  border-radius: 0;
  background: #fff;
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.13), 0 1px 5px 0 rgba(0, 0, 0, 0.08);
  padding: 0 1.6rem;
  color: rgb(75, 75, 76);
  margin-bottom: 0.8rem;
  width: 700px;
}
.card:hover {
  color: rgb(14, 13, 13);
  box-shadow: 0 2px 2px 0 rgba(0, 0, 0, 0.13), 0 3px 5px 0 rgba(0, 0, 0, 0.08);
}
.button {
    display: inline-block;
    text-align: center;
    line-height: 1;
    cursor: pointer;
    -webkit-appearance: none;
    transition: all 0.25s ease-out;
    vertical-align: middle;
    border: 1px solid transparent;
    border-radius: 6px;
    padding: 0.85em 1em;
    margin: 1 2rem 2rem 0;
    font-size: 0.9rem;
    background: #3e34f9;
    color: #FAFAFA;
}
.first {
    margin-top: 1.6rem;
}
</style>

