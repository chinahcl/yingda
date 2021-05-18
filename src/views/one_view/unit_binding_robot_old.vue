<template>
    <div id="unit_binding_robot">
        <el-row>
        <el-col :span="12">
          <!-- <el-form :model="ruleForm" status-icon ref="ruleForm" label-width="100px" class="demo-ruleForm"> -->
            <div class="grid-content bg-purple"><h3 style="color:black">请选择绑定单位</h3>
                <el-select v-model="value" placeholder="请选择" size="big" @change="selectChanged">
                    <el-option
                    v-for="item in options"
                    :key="item.id"
                    :label="item.unit_name"
                    :value="item.id">
                    </el-option>
                </el-select>
                <br>
                <!-- <template> -->
                <el-form-item label="机器人" prop="type">
                  <el-checkbox-group v-model="ruleForm">
                  <el-checkbox v-for="city in cities" :label="city" :key="city" name="type" @change="ruleForm"><h3>{{city}}</h3></el-checkbox>
                  </el-checkbox-group>
                </el-form-item>
              <!-- </template> -->
              <br>
              <!-- <el-button type="primary" @click="submitForm('ruleForm')">确认绑定</el-button> -->
            </div>
            <!-- </el-form> -->
            </el-col>
        <el-col :span="12">
            <div class="grid-content bg-purple-light">
            </div></el-col>
        </el-row>
    </div>
</template>

<script>
// const cityOptions = []
export default {
  data () {
    return {

      ruleForm: [],
      options: [],
      value: '',
      checkedCities: [],
      cities: [],
      isIndeterminate: true,
      checkAll: false
    }
  },
  created () {
    const id = localStorage.use_unit
    this.axios.get('/users', {
    }).then((res) => {
      // if(res.data)
      // Message.success('登陆成功')
      this.options = res.data.data
      console.log(res.data.data)
    }).catch((error) => {
      console.log(error)
    })
    this.axios.get('/robot/' + id, {
      name
    }).then((res) => {
      // if(res.data)
      // Message.success('登陆成功')
      // this.cities = []
      var x
      for (x in res.data.data) {
        console.log('x', res.data.data[x])
        this.cities.push(res.data.data[x].robot_name)
        // this.ruleForm.cities.push(res.data.data[x].robot_name)
      }
      // console.log(res.data.data[0].robot_name)
    }).catch((error) => {
      console.log(error)
    })
  },
  methods: {
    submitForm (city) {
      console.log(city)
    },
    // handleCheckAllChange (val) {
    //   this.checkedCities = val ? cityOptions : []
    //   this.isIndeterminate = false
    // },
    // handleCheckedCitiesChange (value) {
    //   const checkedCount = value.length
    //   this.checkAll = checkedCount === this.cities.length
    //   this.isIndeterminate = checkedCount > 0 && checkedCount < this.cities.length
    // },
    selectChanged (value) {
      console.log(value)
      // this.axios.get('/robot/' + value, {
      // }).then((res) => {
      //   // if(res.data)
      //   // Message.success('登陆成功')
      //   this.cityOptions = res.data.data
      //   console.log(res.data.data)
      // }).catch((error) => {
      //   console.log(error)
      // })
    }
  }
}
</script>

<style scoped>

</style>
