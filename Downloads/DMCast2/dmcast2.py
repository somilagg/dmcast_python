import numpy as np

class wthr_t(object):
    temp = np.empty([1, 24])
    rh = np.empty([1, 24])
    wet = np.empty([1, 24])
    rainfall = np.empty([1, 24])
    wetcnt = np.empty([1, 24])
    wetmins = np.empty([1, 24])
    wettemps = np.empty([1, 24])
    dd7 = 0.0
    dlyrain = 0.0
    dlytemp = 0.0
    ok = np.empty([1, 24])

class cultivar_t(object):
    els = np.empty([1, 367])
    rincb = np.empty([367, 24])
    sincb = np.empty([367, 24])
    els12 = 0.0
    primary_inf = 0.0
    incubation = 0.0
    dmwarns = 0.0

class model_t(object):
    sp = np.empty([1, 24])
    sv = np.empty([1, 24])
    dmrisk = np.empty([1, 24])
    isprd = np.empty([1, 24])
    istmp = np.empty([1, 24])
    spmort = np.empty([1, 24])
    infect = np.empty([1, 24])

class warning_t(object):
    sday = 0
    shour = 0
    eday = 0
    ehour = 0
    duration = 0
    dmrisk = 0.0

class date(object):
    da_year = 0
    da_mon = 0
    da_day = 0

class dmcast2(object):

    def __init__(self):
        self.w = wthr_t()
        self.m = model_t()
        self.wrn = warning_t()
        self.c = cultivar_t()
        self.raw1 = 0.0
        self.raw2 = 0.0
        self.wthr1 = 0.0
        self.wthr2 = 0.0
        self.cyear = 0
        self.nsites = 0
        self.d_temp = 0
        self.d_rh = 0
        self.d_wet = 0
        self.d_rainfall = 0
        self.model_init = 0
        self.dmwarns = 0
        self.day_first = 0
        self.day_last = 0
        self.hour_first = 0
        self.hour_last = 0

    """
    DMCAST.C METHODS
    """
    def MFREE(self, x):
        if x:
            free(x)
            (x) = None

    def free_memory(self):
        MFREE(c)
        MFREE(w)
        MFREE(m)
        MFREE(wrn)
        MFREE(raw)

    """
    CULTIVAR.C METHODS
    """
    def grape_phenology(self, A, B, k, m):
        
        Dday7 = 0.0

        for day in range(1, day_last):
            Dday7 = w[day].dd7
            c[0].els[day] = A * (1 + exp(B-k*Dday7)) ** (1.0/(1.0-m))
            if c[0].els[day] >= 12 and c[0].els12 == 0:
                c[0].els12 = day 

        c[0].els[day_last] = c[0].els[day_last-1]

    def primary_infection(self):

        for day in range (0, day_last):
            if c[0].els[day] >= 12 and w[day].dlyrain > 2.54 and w[day.dlytemp] > 11.1:
                c[0].primary_inf = day 
                break

    def incubation_period(self):
        x = 0.0
        y = 0.0

        for day in range(day_first, day_last+1):
            for hour in range(0, 24):
                if (day == day_first and hour < hour_first) or (day == day_last and hour > hour_last):
                    continue
                if w[day].temp[hour] > 8.0 and w[day].temp[hour] < 35.0:
                    x = w[day].temp[hour]
                    y = 41.961 - 3.5794 * x + 0.09803 * x * x - 0.0005341 * x * x * x
                    if y > 0:
                        rincb = (1.0/y)/24.0
                    else:
                        rincb = 0.0
                    c[0].rincb[day][hour] = rincb
                c[0].sincb[day][hour] = c[0].sincb[day][hour-1] + c[0].rincb[day][hour]
        sincb = 0
        for day in range(c[0].primary_inf, day_last+1):
            for hour in range(0, 24):
                if (day==day_first and hour<hour_first) and (day==day_last and hour>hour_last):
                    break
                c[0].rincb[day][hour] = c[0].rincb[day][hour]
                sincb += c[0].rincb[day][hour]
                c[0].sincb[day][hour] = sincb
                if (sincb > 0.9999):
                    c[0].incubation = day
                    break
                
    """
    WEATHER.C METHODS
    """
    def read_weatherdata(self, endIndex, allDays, allHours, tmp, rh, prcp, lwet, ok):
        for o in range(len(ok)):
            ok[o] = False

        print(endIndex)
        print(len(allDays))
        for index in range(0, endIndex+1):
            day = allDays[index]
            hour = allHours[index]
            w[day].temp[hour] = tmp[index]
            w[day].rh[hour] = rh[index]
            w[day].rainfall[hour] = prcp[index] 
            w[day].wet[hour] = lwet[index] 
            w[day].ok[hour] = ok[index]

        day_first = allDays[0]
        hour_first = allHours[0]
        day_last = allDays[endIndex]
        hour_last = allHours[endIndex]

    def process_weatherdata(self):
        wetsum = 0.0
        wettemps = 0.0
        cnt = 0.0
        tmax = 0.0
        dd7 = 0.0
        wetcnt = 0.0

        for day in range(day_first, day_last+1):
            tmax=0
            cnt=0
            w[day].dlyrain = 0
            w[day].dlytemp = 0

            for hour in range(0, 24):
                if (day==day_first and hour < hour_first) or (day==day_last and hour > hour_last) or (w[day].ok[hour] != True):
                    continue
                if w[day].wet[hour] > 0.1666:
                    wetcnt += 1
                    wetsum += w[day].wet[hour]
                    wettemps += w[day].temp[hour]
                else:
                    wetcnt = 0
                    wetsum = 0
                    wettemps = 0

                w[day].wetcnt[hour] = wetcnt
                w[day].wetmins[hour] = wetsum * 60
                w[day].wettemps[hour] = wettemps

                tmax = max(tmax, w[day].temp[hour])
                w[day].dlyrain += w[day].rainfall[hour]
                cnt += 1
                w[day].dlytemp += (w[day].temp[hour] - w[day].dlytemp) / cnt
            
            dd7 += max((tmax-7), 0)
            w[day].dd7 = dd7
                
    """
    CYCLE.C METHODS
    """
    def sporulation(self, day, hour):
        isprd = 0
        tmpsum = 0.0
        istmp = 0.0
        sp = 0.0

        if model_init:
            isprd = 0
            tmpsum = 0.0

        if (hour <= 21 and hour > 5) or w[day].rh[hour] < 90.0:
            isprd = 0
            tmpsum = 0.0
            istmp = 0.0

        if (hour > 21 or hour <= 5) and w[day].rh[hour] >= 90.0:
            isprd += 1
            tmpsum += w[day].temp[hour]
            istmp = tmpsum/isprd;

            if isprd < 4:
                sp = 0.0
            else:
                if istmp > 13.0 and istmp < 22.5:
                    sp = max( (-642.0 + 53.7*istmp - 0.0356*istmp*istmp*istmp)/160.756 , 0.0 )
                elif istmp >= 22.5 and istmp <= 28.0:
                    sp = 1.0
                elif istmp > 28.0 and istmp < 30.0:
                    sp = 0.1
                else:
                    sp = 0.0
        else:
            sp = 0.0

        m[day].isprd[hour] = isprd
        m[day].istmp[hour] = istmp
        m[day].sp[hour] = sp

    def survival(self, day, hour):
        sv = 0.0
        spmort = 0.0
        t = 0.0

        if model_init:
            sv = 0

        # Set SV to the maximum amount of survival or sporulation.
        if sv < m[day].sp[hour]:
            sv = m[day].sp[hour]
        t = w[day].temp[hour]

        # Calculate SPMORT based on hourly temperature and relative humidity. 
        if w[day].rh[hour] >= 90.0:
            if t <= 25.0:
                spmort = -0.00138 + 0.000496*t
            else:
                spmort = -0.7711 + 0.03126*t
        else:
            spmort = exp( -4.2057 - 0.2101*t + 0.0095*t*t )
        
        spmort = max (spmort, 0.0)

        # Calculate SV. Set SV=0 if SV<0.0;. 
        sv = sv - spmort
        sv = max (sv, 0.0)
        m[day].spmort[hour] = spmort
        m[day].sv[hour] = sv

    def infection(self, day, hour):
        tsumi = 0.0
        infect = 0.0

        tsumi = w[day].wettemps[hour]

        if tsumi<45.0:
            infect=0.0
        elif tsumi>=45.0 and tsumi<50.0:
            infect=(0.3/5.0)*(tsumi-45.0) + 0.2
        elif tsumi>=50.0 and tsumi<71.0:
            infect=(0.5/21.0)*(tsumi-50.0) + 0.5
        else:
            infect=1.0;
        m[day].infect[hour] = infect
        # Determine risk level of disease development */
        m[day].dmrisk[hour] = m[day].sv[hour] * infect * 100

    def calculate_warnings(self, day, hour):
        flag = False
        duration = 0
        duration1 = 0
        sday = 0
        shour = 0

        sumrisk = 0.0
        lastdata = 0

        if model_init: 
            flag = False 
            duration = 0 
            duration1 = 0 
            sday = 0 
            shour = 0 
            dmwarns = 0 
            sumrisk = 0.0 
        

        if w[day].ok[hour] != True: 
            return 0

        if day==day_last and hour==hour_last: 
            lastdata = True;
        else: 
            lastdata = False;

        if m[day].dmrisk[hour] > WARNING: 
            if flag == False:
                sday=day 
                shour=hour
                flag = True
            duration += 1
            duration1 += 1
            sumrisk += m[day].dmrisk[hour]

        if (flag == True) and (m[day].dmrisk[hour] <= WARNING or lastdata):
            wrn[dmwarns].sday=sday
            wrn[dmwarns].shour=shour
            if hour == 0:
                wrn[dmwarns].eday=day-1
                wrn[dmwarns].ehour=23
            else:
                wrn[dmwarns].eday=day
                wrn[dmwarns].ehour=hour-1
            
            wrn[dmwarns].duration=duration1
            wrn[dmwarns].dmrisk=sumrisk/duration
            dmwarns += 1
            duration = 0
            duration1 = 0
            sumrisk = 0.0
            flag = False
            

            # for cultivar specific warnings 
            if day >= c[0].incubation:
                c[0].dmwarns += 1

    def run_disease_model(self, w_sday, w_shour, w_eday, w_ehour, w_duration, w_params):
        for day in range(day_first, day_last+1):
            for hour in range(0, 24):
                if (day == day_first and hour < hour_first) or (day == day_last and hour > hour_last):
                    continue
                sporulation(day,hour)
                survival(day,hour)
                infection(day,hour)
                calculate_warnings(day,hour)
                if (model_init):
                    model_init = False

        for day in range(0, dmwarns+1):
            w_sday[day] = wrn[day].sday
            w_shour[day] = wrn[day].shour
            w_eday[day] = wrn[day].eday
            w_ehour[day] = wrn[day].ehour
            w_duration[day] = wrn[day].duration

        w_parms[0] = dmwarns
        w_parms[1] = c[0].els12
        w_parms[2] = c[0].primary_inf
        w_parms[3] = c[0].incubation

    """
    MISC.C METHODS
    """
    def isleap(self, year):
        if year % 400 == 0:
            return 1
        if year % 100 == 0:
            return 0
        if year % 4 == 0:
            return 1

        return 0

    def gre2jul(self, d):
        month = [0,31,28,31,30,31,30,31,31,30,31,30,31]
        jd=0

        month[2] += self.isleap(d.da_year)

        for i in range(1, 13):
            jd += month[i]
      
        jd += d.da_mon  
        return jd

    def jul2gre(self, jd, d):
        month =[0,31,28,31,30,31,30,31,31,30,31,30,31]
        i=1

        month[2] += self.isleap(d.da_year)
        month[0] = jd
        while( (jd - month[i]) > 0 ):
            jd -= month[i]
            i += 1
        
        d.da_mon = i
        d.da_day = jd
        if( (d.da_day > 31) or (i > 12) ):
            printf("Given day of year (%d) invalid", month[0])
        
        return d

    '''
    def jul2tm(self, year, day, hour, tm):
        month = [31,28,31,30,31,30,31,31,30,31,30,31]

        tm.tm_sec = 0
        tm.tm_min = hour % 100
        tm.tm_hour= hour / 100
        tm.tm_year= year - 1900
        tm.tm_isdst = 0
        
        month[1] += self.isleap(year)
        i=0
        while( (i < 11) and ((day - month[i]) > 0) ):
            day -= month[i]
            i += 1
        
        tm.tm_mon = i
        tm.tm_mday = day
        if(tm.tm_mday > 31):
            printf("Given day of year (%d) invalid", month[0])
            return None
        
        return tm
    '''
    '''
    def jul2utime(year, day, tod):
        time_ptr = tm()
        month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        # is it leap year?
        month[1] += self.isleap(year)

        for i in range(0, 11):
            if day - month[i] > 0:
                day -= month[i]

        time_ptr.tm_sec = 0
        time_ptr.tm_min = tod % 100
        time_ptr.tm_hour = tod / 100
        time_ptr.tm_mday = day
        time_ptr.tm_mon = i
        time_ptr.tm_year = year - 1900
        time_ptr.tm_isdst = 0

        return time_ptr
    '''