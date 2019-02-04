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


