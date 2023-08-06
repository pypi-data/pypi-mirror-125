(function() {
    var app = new Vue({
        el: '#app',
        data(){
        return {
                config: {},
                defaultTemperatures: [5, 20, 25]
            }
        },
        async mounted() {
            this.config = (await axios.get('/api/config')).data;
            // https://stackoverflow.com/a/55379279
            this.config.thermostats.forEach(t => this.$set(t, 'temperature', 22));
         },
        methods: {
            wakeupHost: (name) => {
                axios
                  .post('/api/wake-on-lan', {
                    name: name
                  })
            },
            changeToAutomatic: (name) => {
                axios
                  .post('/api/thermostats/change-to-automatic', {
                    name: name
                  })
            },
            enableBoost: (name) => {
                axios
                  .post('/api/thermostats/set-boost', {
                    name: name
                  })
            },
            changeTemperatureTo: (name, temperature) => {
                axios
                  .post('/api/thermostats/change-temperature', {
                    name: name,
                    temperature: temperature
                  })
                  .catch((error) => {
                      console.log(this);
                  });
            }
        }
    });
})();