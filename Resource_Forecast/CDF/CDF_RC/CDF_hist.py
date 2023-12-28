import pandas as pd
import  numpy as np

predict_95p=pd.read_parquet('D://cluster-resource-forecast-master//Data//output//prediction_24hr_high_rc_machine_like_predictor_95-00000-of-00001.parquet').rename(columns={"predicted_peak": "rc_like_machine_95"})
predict_90p=pd.read_parquet('D://cluster-resource-forecast-master//Data//output//prediction_24hr_high_rc_machine_like_predictor_90-00000-of-00001.parquet').rename(columns={"predicted_peak": "rc_like_machine_90"})
predict_85p=pd.read_parquet('D://cluster-resource-forecast-master//Data//output//prediction_24hr_high_rc_vm_like_predictor_85-00000-of-00001.parquet').rename(columns={"predicted_peak": "rc_like_vm_85"})

predict_95p["simulated_time"]=predict_95p["simulated_time"]/predict_95p["simulated_time"].min()
predict_90p["simulated_time"]=predict_90p["simulated_time"]/predict_90p["simulated_time"].min()
predict_85p["simulated_time"]=predict_85p["simulated_time"]/predict_85p["simulated_time"].min()

predict_=pd.read_parquet('D://cluster-resource-forecast-master//Data//output//prediction_2hr_all.parquet')

all=pd.merge(predict_[["simulated_time","simulated_machine","oracle","rc_like_vm","limit"]],predict_95p[["simulated_time","simulated_machine","rc_like_machine_95"]],on=["simulated_time","simulated_machine"])
all=pd.merge(all,predict_90p[["simulated_time","simulated_machine","rc_like_machine_90"]],on=["simulated_time","simulated_machine"])
all=pd.merge(all,predict_85p[["simulated_time","simulated_machine","rc_like_vm_85"]],on=["simulated_time","simulated_machine"])
#all["borg"]=all["limit"]*0.9
#all["max"]=all[['nsigma','rc_like_machine', 'rc_like_vm', 'borg']].max(axis=1)
all["simulated_time"]=all["simulated_time"]/all["simulated_time"].min()
#all=pd.merge(all,predict_ml,on="simulated_time")

#all.to_parquet("./prediction_2hr_all.parquet")
#print(predict_)


from sklearn.metrics import mean_absolute_percentage_error,mean_squared_error

#all=pd.read_parquet("D://cluster-resource-forecast-master//prediction_2hr_all.parquet")
algo_serial=dict()
#algo_serial["nsigma"]=0
algo_serial["rc_like_vm"]=0
algo_serial["rc_like_vm_85"]=1
#algo_serial["max"]=4



def output_predictions(predictors,true,limit):
    prd = []
    sav = []
    vio = []
    vio_sev = []
    mse = []
    mape = []
    for predictor in predictors.keys():
        prd.append(predictor)
        pred_vals=np.array([[predictors[predictor][x]] for x in range(len(predictors[predictor].values()))])
        output=dict()
        output["mse"]=mean_squared_error(pred_vals,true)
        mse.append(output["mse"])
        output["mape"]=mean_absolute_percentage_error(pred_vals,true)
        mape.append(output["mape"])
        output["savings"]=((limit-pred_vals)).clip(min=0).sum()/limit.sum()
        sav.append(output["savings"])
        output["violations"]= np.where(np.array(true)>pred_vals,1,0).sum()/len(true)
        vio.append(output["violations"])
        output["violation_severity"]= np.where(np.array(true)>np.array(pred_vals),((np.array(true)-np.array(pred_vals))),0).sum()/np.array(true).sum()
        vio_sev.append(output["violation_severity"])
        print(predictor)
        print(output)
        #np.where(((np.array(ot_true)-np.array(ot_pred))/np.array(ot_true))<0,0,((np.array(ot_true)-np.array(ot_pred))/np.array(ot_true))).sum()
    print(prd)
    print(sav)
    print(vio)
    print(vio_sev)
    print(mse)
    print(mape)
    return sav,vio,vio_sev

algo_to_consider=['rc_like_vm','rc_like_vm_85']

output_predictions(all[algo_to_consider].to_dict(),all[["oracle"]].to_numpy(),all[["limit"]].to_numpy())
cum_vio=dict()
cum_vio_sev=dict()
cum_sav=dict()
cum_machine_no=[]
total_machines=len(all["simulated_machine"].unique())
current_machine=0

for machine_id, current_machine_data in all.groupby(["simulated_machine"]):
    current_machine+=1
    cum_machine_no.append(current_machine/total_machines)
    machine_algo_result=current_machine_data.copy().reset_index().drop("index",axis=1)
    machine_sav,machine_vio,machine_vio_sev=output_predictions(machine_algo_result[algo_to_consider].to_dict(),machine_algo_result[["oracle"]].to_numpy(),machine_algo_result[["limit"]].to_numpy())

    for key in algo_serial.keys():
        if(key in cum_sav.keys()):
            cum_sav[key].append(machine_sav[algo_serial[key]])
        else:
            cum_sav[key] = [machine_sav[algo_serial[key]]]

        if(key in cum_vio.keys()):
            cum_vio[key].append(machine_vio[algo_serial[key]])
        else:
            cum_vio[key] = [machine_vio[algo_serial[key]]]

        if(key in cum_vio_sev.keys()):
            cum_vio_sev[key].append(machine_vio_sev[algo_serial[key]])
        else:
            cum_vio_sev[key] = [machine_vio_sev[algo_serial[key]]]


print(cum_machine_no)
print(cum_sav)
print(cum_vio)
print(cum_vio_sev)

from matplotlib import pyplot as plt
plt.rcParams["figure.figsize"] = [8,6]
plt.rcParams["figure.autolayout"] = True

def draw_cdf(data,file_name):
    for key in data.keys():
        N = len(data[key])
        values = np.array(data[key])
        #count, bins_count = np.histogram(values, bins=N)
        #pdf = count / sum(count)
        #cdf = np.cumsum(pdf)
        plt.hist(values, label=key)

    #plt.xlim(0,1)
    #plt.ylim(0,1)
    #plt.xlabel("Per Machine "+file_name)
    #plt.gca().axes.get_xticklabels()[0].set_visible(False)
    plt.legend()
    plt.savefig("./output/"+file_name+"vm.jpg")
    plt.show()
    plt.cla()
    plt.clf()
    #plt.show()
draw_cdf(cum_sav,"Savings")
draw_cdf(cum_vio,"Violations")
draw_cdf(cum_vio_sev,"Violation Severity")
print(cum_vio_sev)
