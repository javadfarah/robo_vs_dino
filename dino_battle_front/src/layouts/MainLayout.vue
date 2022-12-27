<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>


        <q-toolbar-title>
          dino battle
        </q-toolbar-title>


      </q-toolbar>

    </q-header>

    <q-page-sticky position="top-left" :offset="[18, 18]">
      <div class="q-pa-md q-gutter-y-md column items-start">
        <q-btn-group push>
          <q-btn color="green-8" push label="new game" icon="add_circle" @click="new_game"/>
          <q-btn color="red-7" push label="reset" icon="replay" @click="new_game"/>

        </q-btn-group>

      </div>
      <div class="q-px-xs q-pb-md">
        <q-timeline :layout="layout" color="secondary">
          <q-timeline-entry heading>
            how to play
          </q-timeline-entry>

          <q-timeline-entry
            subtitle="insert"
            side="left"
          >
            <div>
              for insert new creature
              <br>
              you can <u>right_click</u> on empty cells
            </div>
          </q-timeline-entry>

          <q-timeline-entry
            subtitle="action"
            side="left"
          >
            <div>
              for doing an action [move, attack]
              <br>
              you can click on dinosaur cells
            </div>
          </q-timeline-entry>
        </q-timeline>
      </div>
    </q-page-sticky>
    <template v-if="land_grid_objects.length<1">
    </template>

    <template v-else>


      <div class="q-pa-md absolute-center" style="max-width: 800px;padding-top: 10%"
           @contextmenu.prevent="r_click_disable">

        <div class="q-gutter-x-md q-gutter-y-s">
          <div v-for="index1 in land_count" :key="index1" class="row">
            <q-btn color="purple" v-for="index2 in land_count" :key="index2" label=""
                   class="col-1" :icon="get_land_content(index1+':'+index2)">
              <template v-if="get_land_content(index1+':'+index2)=='smart_toy'">
                <q-menu v-close-popup

                >
                  <q-list style="min-width: 100px">

                    <q-item clickable>

                      <q-item-section @click="attack(index1,index2)">attack</q-item-section>
                    </q-item>
                    <q-item clickable>
                      <q-item-section @click="move(index1,index2,'left')">left</q-item-section>
                    </q-item>
                    <q-item clickable>
                      <q-item-section @click="move(index1,index2,'right')">right</q-item-section>
                    </q-item>
                    <q-item clickable>
                      <q-item-section @click="move(index1,index2,'up')">up</q-item-section>
                    </q-item>
                    <q-item clickable>
                      <q-item-section @click="move(index1,index2,'down')">down</q-item-section>
                    </q-item>


                  </q-list>
                </q-menu>
              </template>
              <template v-else-if="get_land_content(index1+':'+index2)=='pets'"></template>
              <template v-else>
                <q-menu
                  touch-position
                  context-menu
                >
                  <q-item clickable>
                    <q-item-section @click="insert_creature(index1+':'+index2,'dino')">insert dino</q-item-section>
                  </q-item>
                  <q-item clickable>
                    <q-item-section @click="insert_creature(index1+':'+index2,'robo')">insert robo</q-item-section>
                  </q-item>
                </q-menu>
              </template>
            </q-btn>
          </div>
        </div>
      </div>
    </template>
  </q-layout>
</template>

<script>
import {defineComponent, ref} from 'vue'
import EssentialLink from 'components/EssentialLink.vue'
import axios from "axios";
import {useQuasar} from "quasar";

export default defineComponent({
  name: 'MainLayout',

  components: {},

  setup() {
    const $q = ref(useQuasar());
    const land_count = 0
    return {
      land_count: ref(land_count),
      land_grid_objects: ref(Array),
      show_menu: ref(true)
    }
  },
  methods: {
    r_click_disable() {
    }
    ,
    move(x, y, direction) {
      axios
        .put("http://127.0.0.1:8000/land/action/move/", {x: x, y: y, direction: direction})
        .then((response) => {
          this.get_land()
        })
        .catch((e) => {
          this.$q.notify({
            progress: true,
            message: e.response.data.message,
            icon: "report_problem",
            color: "negative",
            textColor: "white",
          });

        });
    },
    attack(x, y) {
      axios
        .put("http://127.0.0.1:8000/land/action/attack/", {x: x, y: y})
        .then((response) => {
          this.get_land()
        }).catch((e) => {
        this.$q.notify({
          progress: true,
          message: e.response.data.message,
          icon: "report_problem",
          color: "negative",
          textColor: "white",
        });
        this.submitting = false;

        console.log(e);
      });
    },
    insert_creature(key, content) {
      axios
        .put("http://127.0.0.1:8000/land/insert/", {content: content, position: key})
        .then((response) => {
          this.get_land()
        })
        .catch((e) => {
          this.$q.notify({
            progress: true,
            message: "server failure! please try again later",
            icon: "report_problem",
            color: "negative",
            textColor: "white",
          });
        });
    },
    create_land() {
      axios
        .post("http://127.0.0.1:8000/land/")
        .then((response) => {
          this.get_land()
        })
        .catch((e) => {
          this.$q.notify({
            progress: true,
            message: "server failure! please try again later",
            icon: "report_problem",
            color: "negative",
            textColor: "white",
          });
        });
    },
    new_game() {
      axios
        .delete("http://127.0.0.1:8000/land/")
        .then((response) => {
          this.create_land()
        })
        .catch((e) => {
          this.$q.notify({
            progress: true,
            message: "server failure! please try again later",
            icon: "report_problem",
            color: "negative",
            textColor: "white",
          });
        });
    },
    get_land_content(position) {
      let obj = this.land_grid_objects.find(o => o.id === position);
      if (obj.content != null && obj.content.toLowerCase() == 'dino') {
        return "pets"
      }
      if (obj.content != null && obj.content.toLowerCase() == 'robo') {
        return "smart_toy"
      }

      return obj.content
    },
    get_land() {
      this.show_menu = false;
      axios
        .get("http://127.0.0.1:8000/land")
        .then((response) => {
          this.land_grid_objects = response.data.data.items
          this.land_count = response.data.data.count
        })
        .catch((e) => {
          this.$q.notify({
            progress: true,
            message: "server failure! please try again later",
            icon: "report_problem",
            color: "negative",
            textColor: "white",
          });

        });
      this.show_menu = true;
    }

  },
  mounted() {
    this.get_land()
  }
})
</script>
