import { createRouter, createWebHistory } from 'vue-router'
import DatabaseView from '../views/DatabaseView.vue'
import AddServicesView from '../views/AddServicesView.vue'
import BuildServicesView from '../views/BuildServicesView.vue'
import ReportHistoryView from '../views/ReportHistoryView.vue'
import GenerateReportView from '../views/GenerateReportView.vue'
import LoginView from '../views/LoginView.vue'

const routes = [
  {
    path: '/MusicLibrary',
    name: 'Music Library',
    component: DatabaseView,
  },
  {
    path: '/addservice',
    name: 'Add Service',
    component: AddServicesView,
  },
  {
    path: '/buildservice',
    name: 'Build Service',
    component: BuildServicesView,
  },
  {
    path: '/reporthistory',
    name: 'Report History',
    component: ReportHistoryView,
  },
  {
    path: '/generatereport',
    name: 'Generate Report',
    component: GenerateReportView,
  },
  {
    path: '/',
    name: 'Login View',
    component: LoginView,
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

export default router
