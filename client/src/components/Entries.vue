<template>
  <div class="entries">
    <div class="entry" v-for="e in entries" :key="e.id">
      <h3 class="entry-title">
        <router-link
          :to="{
            name: 'EntryView',
            params: { entryid: e._id.$oid },
          }"
        >
          {{ e.title }}
        </router-link>
      </h3>
      <p>
        {{ trimContent(e.content) }}
      </p>

      <div class="cont-btn">
        <router-link
          :to="{
            name: 'EntryView',
            params: { entryid: e._id.$oid },
          }"
        >
          more >
        </router-link>
      </div>
    </div>
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
    getEntries() {
      const path = "http://127.0.0.1:5000/entries";
      this.$http
        .get(path)
        .then((res) => {
          this.entries = res.data;
        })
        .catch((error) => {
          if (error) {
            console.error(error);
          }
        });
    },
    trimContent(content) {
      //regex to show the some part of content
      let trimmed = content.replace(/^(.{250}[^\s]*).*/, "$1 ...");
      return trimmed;
    },
  },

  created() {
    this.getEntries();
  },
};
</script>
<style>
.entries .entry {
  margin: 0 auto;
  width: 50%;
}
.entries .entry .entry-title {
  font-size: 1.5rem;
  color: var(--blue);
}
.entries .entry .entry-title a {
  color: var(--blue);
}
.entries .entry .cont-btn {
  margin-top: 5px;
  margin-bottom: 15px;
  font-size: 0.8rem;
}
.entries .entry .cont-btn a {
  color: var(--pink);
}
@media only screen and (max-width: 600px) {
  .entries .entry {
    margin: 0 auto;
    width: 80%;
  }
}
</style>
