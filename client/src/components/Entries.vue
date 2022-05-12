<template>
  <div class="entries">
    <ul v-for="e in entries" :key="e.id">
      <li>
        <h3>
          <router-link
            :to="{
              name: 'EntryView',
              params: { entryid: e._id.$oid },
            }"
          >
            {{ e.title }}
          </router-link>
        </h3>
        <p>{{ e.content }}</p>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: "Entries",
  data() {
    return {
      entries: "",
    };
  },
  methods: {
    getMessage() {
      const path = "http://127.0.0.1:5000/entries";
      this.$http
        .get(path)
        .then((res) => {
          this.entries = res.data;
          console.log(this.entries);
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
  created() {
    this.getMessage();
  },
};
</script>
<style>
ul {
  list-style-type: none;
}
.entries {
  width: 50%;
  align-self: center;
}
</style>
