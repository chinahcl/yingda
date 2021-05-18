<template>
    <div>
        <el-row>
            <el-col :span="12">
                <div class="grid-content bg-purple">
                    <el-form ref="form" :model="form" label-width="180px" status-icon>
                        <el-form-item label="请选择绑定单位">
                            <el-select @change="selectChanged" v-model="form.region" placeholder="请选择">
                            <el-option v-for="item in options" :key="item.id" :label="item.unit_name" :value="item.id"></el-option>
                            </el-select>
                        </el-form-item>
                        <el-form-item label="选择绑定机器人">
                            <el-checkbox-group v-model="form.type">
                            <el-checkbox v-for="city in cities" :label="city" :key="city" name="type">{{city}}</el-checkbox>
                            </el-checkbox-group>
                        </el-form-item>
                        <el-form-item>
                            <el-button type="primary" @click="submitForm('Form')">立即创建</el-button>
                            <!-- <el-button>取消</el-button> -->
                        </el-form-item>
                </el-form>
                </div></el-col>
            <el-col :span="12">
                <div class="grid-content bg-purple-light">
                    <template>
                    <el-table
                        :data="tableData"
                        style="width: 100%"
                        :row-class-name="tableRowClassName">
                        <el-table-column
                        prop="data"
                        label="日期">
                        </el-table-column>
                        <el-table-column
                        prop="unit_name_id"
                        label="单位名称">
                        </el-table-column>
                        <el-table-column
                        prop="robot_id"
                        label="机器人名称">
                        </el-table-column>
                    </el-table>
                    </template>
                </div></el-col>
        </el-row>

    </div>
</template>

<script>
import { Message } from 'element-ui'
export default {
  data () {
    return {
      name: localStorage.yun_user.replace('"', "'").replace('"', "'"),
      tableData: [],
      cities: [],
      options: [],
      form: {
        region: '',
        type: []
      }
    }
  },
  created () {
    const id = localStorage.use_unit
    const name = this.name
    this.axios.get('/users', {
    }).then((res) => {
      this.options = res.data.data
      console.log(res.data.data)
    }).catch((error) => {
      console.log(error)
    })
    this.axios.get('/robotapi/' + id, {
      name
    }).then((res) => {
      var x
      for (x in res.data.data) {
        console.log('x', res.data.data[x])
        this.cities.push(res.data.data[x].robot_name)
      }
    }).catch((error) => {
      console.log(error)
    })
    this.axios.get('/users/intermediate/' + 0, {}).then((res) => {
      console.log('res', res)
      this.tableData = res.data.data
    })
  },
  methods: {
    selectChanged (value) {
      console.log(value)
      this.axios.get('/users/intermediate/' + value, {}).then((res) => {
        console.log(res)
        this.form.type = res.data.data
      })
    },
    submitForm (form) {
      if (form) {
        const data = this.form
        this.axios.post('/users/intermediate/' + 1, {
          data
        }).then((res) => {
          if (res.data.code === 1) {
            Message.success('增加成功')
            // this.tableData = res.data.data
            console.log(res.data)
            location.reload()
          } else {
            Message.warning('重复账号')
          }
        }).catch((error) => {
          console.log(error)
        })
      } else {
        console.log('无数据')
      }
    },
    tableRowClassName ({ row, rowIndex }) {
      if (rowIndex === 1) {
        return 'warning-row'
      } else if (rowIndex === 3) {
        return 'success-row'
      }
      return ''
    }
  }
}
</script>

<style scoped>
.el-table .warning-row {
    background: oldlace;
  }

  .el-table .success-row {
    background: #f0f9eb;
  }
</style>
