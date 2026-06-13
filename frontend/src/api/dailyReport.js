import { http } from './http'

export const dailyReportApi = {
  get: (reportDate) => http.get(reportDate ? `/daily-report?report_date=${reportDate}` : '/daily-report'),
}
