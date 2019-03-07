<template>
  <div class="header">
    <h1 class="cover-heading ">JARIS</h1>
    <!-- <b-form @submit="onSubmit" @reset="onReset" >
      <b-form-group id="Inp1"
                    label-sr-only
                    label-for="Inp1">
        <b-form-input id="Inp2"
                      type="text"
                      v-model="form.name"
                      required
                      placeholder="Type here and press Enter">
        </b-form-input> -->
      <!-- </b-form-group> -->

      <b-button class = "button" variant="primary" v-show="btn && !btnReset" v-on:click="startRecording">Start Recording</b-button>
      <b-button class = "button" variant="danger" v-show="btnStop" v-on:click="stopRecording">Stop</b-button>
      <b-button class = "button" variant="danger" v-show="btnReset" v-on:click="redirectError">Reset</b-button>

    <!-- </b-form> -->

    <b-card class="text">
   {{textResult}}
    </b-card>

  </div>

</template>

<script>
  var audioContext = new(window.AudioContext || window.webkitAudioContext)();
  var socket = io.connect('http://localhost:5000');
  //var socket = io.connect('http://167.99.3.111:5002');
  var ssStream = ss.createStream();
  var scriptNode;
  
  export default {
    // inject: ['reload'],
    data() {
      return {
        btn: true,
        btnStop: false,
        btnReset: false,
        result: false,
        resultError: false,
        textResult: "",
        selected: 'en-US',
        items: [
          {
            text: 'English (United States)',
            value: 'en-US'
          }
        ]
      }
    },
    methods: {
      successCallback(stream) {
        const vm = this;
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
        
          that.textResult = text;
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
