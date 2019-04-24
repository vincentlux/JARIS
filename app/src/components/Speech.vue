<template>
  <div class="header">
    <h1 class="cover-heading ">J.A.R.I.S</h1>
    <h4 style="margin-bottom: 1.5rem">"Just Another Really Intelligent System"</h4>
    <b-form @submit="onSubmit" class="mx-auto" style="width: 700px;">
      <b-form-group id="Inp1"
                    label-sr-only
                    label-for="Inp1">
        <b-form-input id="Inp2"
                      size="lg"
                      type="text"
                      v-model="form.name"
                      required
                      placeholder="">
        </b-form-input>
      </b-form-group>

      <b-button class = "button" variant="primary" v-show="btn && !btnReset" v-on:click="startRecording">Start Recording</b-button>
      <b-button class = "button" variant="danger" v-show="btnStop" v-on:click="stopRecording">Stop</b-button>
      <b-button class = "button" variant="danger" v-show="btnReset" v-on:click="redirectError">Reset</b-button>

    </b-form>

    <!-- <b-card class="text">
   {{this.resObj}}
    </b-card> -->

    <b-card class="text mx-auto first" v-show="isResult&noError" >
      <div>Fetched  {{ this.numBefore }} doc(s) after search </div>

      <div>Returned {{ this.numAfter }} doc(s) after network algorithm</div>
    </b-card>
    <div class="searchResult mx-auto" v-show="isResult&noError" transition="expand" style="width: 700px;">
          <a v-for="elem in resObj" :key="elem.message_id">

      <b-card no-body>
          <h3 class="card-text">{{ Number(elem.doc_id)+1 }}</h3>

          <!-- <p class="card-text">
              From: {{ elem.from[0] }}
              From_name: {{ elem.from_name[0].replace(/ *\<[^>]*\> */g, "") }}
          </p> -->

          <p class="card-text">
              {{ elem.content[0] }}
          </p>
      </b-card>
      </a>
    </div>

  </div>

</template>

<script>
  import axios from 'axios';
  var audioContext = new(window.AudioContext || window.webkitAudioContext)();
  var socket = io.connect('http://localhost:5000');
  //var socket = io.connect('http://167.99.3.111:5002');
  var ssStream = ss.createStream();
  var scriptNode;
  
  export default {
    // inject: ['reload'],
    data() {
      return {
        form: {
          name: '',
        },
        btn: true,
        btnStop: false,
        btnReset: false,
        result: false,
        resObj: null,
        numBefore: 0,
        numAfter: 0,
        resultError: false,
        textResult: "",
        selected: 'en-US',
        isResult:false,
        noError:true,
        firstLoad: true,
        items: [
          {
            text: 'English (United States)',
            value: 'en-US'
          }
        ]
      }
    },
    methods: {
      fetchResult(query){
        // console.log(JSON.stringify(query));
        //const path = 'http://167.99.3.111:5001/simple';
        const path = 'http://localhost:5001/speech';
        // Axios
        console.log(query)
        axios.post(path, query)
          .then((res)=>{
            console.log("success")
            this.numBefore = res.data.QNum;
            this.numAfter = Object.keys(res.data.docs).length;
            this.resObj = res.data.docs;
            console.log(this.resObj)
            this.isResult = true;
            this.noError = true;
          })
          .catch((error) => {
            // this.errMsg =  error.response.data.message;
            this.noError = false;
          });
      },
      onSubmit () {
        // fake submit
        const query = {query:this.form.name};
        console.log(query);
        this.firstLoad = false;
        this.isResult = false;
        this.fetchResult(query);
      },
      successCallback(stream) {
        const vm = this;
        console.log('successCallback:...IN');
        console.log('successCallback:...IN');
        // add user gesture
        console.log(audioContext.resume());
        var input = audioContext.createMediaStreamSource(stream);
        //console.log(input)
        var bufferSize = 2048;
        scriptNode = audioContext.createScriptProcessor(bufferSize, 1, 1);
        scriptNode.onaudioprocess = scriptNodeProcess;
        input.connect(scriptNode);
  
        // console.log('ScriptNode BufferSize:', scriptNode.bufferSize);
        function scriptNodeProcess(audioProcessingEvent) {
        var inputBuffer = audioProcessingEvent.inputBuffer;
        var outputBuffer = audioProcessingEvent.outputBuffer;
        var inputData = inputBuffer.getChannelData(0);
        var outputData = outputBuffer.getChannelData(0);

  
        // Loop through the 4096 samples
        for (var sample = 0; sample < inputBuffer.length; sample++) {
          outputData[sample] = inputData[sample];
        }
        ssStream.write(new ss.Buffer(vm.downsampleBuffer(inputData, 44100, 16000)));
      }
      },
      downsampleBuffer(buffer, sampleRate, outSampleRate) {
        if (outSampleRate == sampleRate) {
          return buffer;
        }
        if (outSampleRate > sampleRate) {
          throw "downsampling rate show be smaller than original sample rate";
        }
        var sampleRateRatio = sampleRate / outSampleRate;
        var newLength = Math.round(buffer.length / sampleRateRatio);
        var result = new Int16Array(newLength);
        var offsetResult = 0;
        var offsetBuffer = 0;
        while (offsetResult < result.length) {
          var nextOffsetBuffer = Math.round((offsetResult + 1) * sampleRateRatio);
          var accum = 0,
            count = 0;
          for (var i = offsetBuffer; i < nextOffsetBuffer && i < buffer.length; i++) {
            accum += buffer[i];
            count++;
          }
  
          result[offsetResult] = Math.min(1, accum / count) * 0x7FFF;
          offsetResult++;
          offsetBuffer = nextOffsetBuffer;
        }
        return result.buffer;
      },
      startRecording() {
        console.log("recording!!");
        // as
        // const languageSelected = this.selected;
        // socket.emit('LANGUAGE_SPEECH', languageSelected);
        this.result = true;
        this.btn = false;
        this.btnStop = true;
        this.btnReset = false;
        scriptNode.connect(audioContext.destination);
        console.log(audioContext.destination);
        console.log("START_SPEECH"); 
        ss(socket).emit('START_SPEECH', ssStream);
        setInterval(function() {
          this.stopRecording();
        }.bind(this), 55000);
      },
      stopRecording() {
        console.log("Stop recording!");
        //console.log("sh")
        this.btnStop = false;
        this.btn = true;
        this.btnReset = true;
        console.log(audioContext.destination);
        scriptNode.disconnect(audioContext.destination);
        ssStream.end();
        socket.emit('STOP_SPEECH', {});
        this.onSubmit();
      },
      errorCallback(error) {
        // console.log('errorCallback:', error);
      },
      redirectError(){
         window.location.href = "http://localhost:8080/"
      },
      // reloadPage(){
      //   this.reload();
      // },
    },

    created() {
      const that = this;
      console.log(audioContext) 
      // console.log("created")
      // console.log(that.result, that.btn, that.btnStop);
      socket.on('SPEECH_RESULTS', function(text) {
        // console.log(text)
        if('q' == text){

          that.resultError = true;
          console.log("error")
        }else{
          // console.log(text)
        
          that.form.name = text;
          // console.log("text:")
          // console.log("2")
          // // console.log(text)
        }
      })
        if (navigator.mediaDevices.getUserMedia) {
          // console.log('getUserMedia supported...');
          navigator.webkitGetUserMedia({ audio: true }, function(stream) {
            // console.log("stream?");
            // // console.log(stream);
            that.successCallback(stream)
          }, function(error) {
            // console.log("error2")
            that.errorCallback(error)
          });
        } else {
          // console.log('getUserMedia not supported on your browser!');
        }
      }
    }
</script>


<style>
  .slide-enter {
    opacity: 0;
  }
  
  .slide-enter-active {
    animation: slide-in 1s ease-out forwards;
    transition: opacity .5s;
  }
  
  .slide-move {
    transition: transform 1s;
  }
  
  @keyframes slide-in {
    from {
      transform: translateY(20px);
    }
    to {
      transform: translateY(0);
    }
  }
</style>
