

def updata_centroid_k(X):
    V=X[:, 0][:, np.newaxis]
    A=X[:, 1][:, np.newaxis]
    # S=X[:, 2][:, np.newaxis]
    S=X[:, 2]
    S=S[np.where(S < 50)]
    S=S[:, np.newaxis]
    k_predict_data=[V,A,S]
    k=0
    k_array=[]
    for data in k_predict_data:

        model = KernelDensity(bandwidth=3, kernel='gaussian')
        model.fit(data)
        x_range = np.linspace(data.min() , data.max(), 500 )
        x_log_prob = model.score_samples(x_range[:, np.newaxis])
        x_prob = np.exp(x_log_prob)
        greater=argrelextrema(x_prob, np.greater)
        l=len(greater[0])
        k_array=np.append(k_array,l)
    k_min=np.min(k_array)
    k_max=np.max(k_array)
    a=int(k_min)+1
    b=int(k_max+k_min)+2
    F=0
    for n in range(2,b,1):
        # print(n)
        kmeans = KMeans(n_clusters=n,random_state=0).fit(X)
        a=len(np.unique(kmeans.labels_))
        if a==1 :
            k=2
        else:
            sc= silhouette_score(X,kmeans.labels_)

            if sc > F:
                F=sc
                k=n
    print("k is:",k)
    return k

def set_weight(mu,n):
    time_array=np.arange(1, n+1, 1)
    weight=[]
    for t in time_array:
        t=float(t)
        # print(mu)
        w=1-2**(-mu*t)

        weight=np.append(weight,w)
    return weight

def find_clusters(C_array,X):

    centroid_label = pairwise_distances_argmin_min(X,C_array)
    centroid_label = centroid_label[0]
    return centroid_label

def factor_generator(x_prior,x_post):
    js_score=[]
    for i in range(0,3):
        x_prior_=x_prior[:,i]
        x_prior_=x_prior_[:,np.newaxis]
        x_post_=x_post[:,i]
        x_post_=x_post_[:,np.newaxis]
        js=caculate_jensenshannon(x_prior_,x_post_)
        js_score=np.append(js_score,js)
    js_score=np.max(js_score)
    return js_score

def caculate_kl(x_prior,x_post):

    model_prior = KernelDensity(bandwidth=1, kernel='gaussian')
    model_prior.fit(x_prior)
    model_post = KernelDensity(bandwidth=1, kernel='gaussian')
    model_post.fit(x_post)
    min_ = min(x_prior.min(), x_post.min())
    max_ = max(x_prior.max(), x_post.max())
    x_range= np.linspace(start=min_, stop=max_, num=500)

    y_log_prior = model_prior.score_samples(x_range[:, np.newaxis])
    y_prior= np.exp(y_log_prior)
    y_log_post = model_post.score_samples(x_range[:, np.newaxis])
    y_post = np.exp(y_log_post)
    kl = scipy.stats.entropy(y_prior, y_post)
    return kl

def caculate_jensenshannon(x_prior,x_post):
    model_prior = KernelDensity(bandwidth=1, kernel='gaussian')
    model_prior.fit(x_prior)
    model_post = KernelDensity(bandwidth=1, kernel='gaussian')
    model_post.fit(x_post)
    min_ = min(x_prior.min(), x_post.min())
    max_ = max(x_prior.max(), x_post.max())
    x_range= np.linspace(start=min_, stop=max_, num=500)

    y_log_prior = model_prior.score_samples(x_range[:, np.newaxis])
    y_prior= np.exp(y_log_prior)
    y_log_post = model_post.score_samples(x_range[:, np.newaxis])
    y_post = np.exp(y_log_post)
    js = jensenshannon(y_prior, y_post)
    return js

def Initialize_the_centroid(Bigdata):
    X_1=Bigdata[0:n]
    kernel= updata_centroid_k(X_1)
    kmeans = KMeans(n_clusters=kernel, random_state=0).fit(X_1)
    C=np.insert(X_1,0,kmeans.labels_,axis=1)
    label=kmeans.labels_
    C_array=[]
    id=np.unique(C[:,0])

    for i in id:
        c_average= C[np.where(C[:, 0] == i)]
        c_average=cal_Cmass(c_average)
        print(type(c_average))
        C_array=np.append(C_array,c_average[1:4])
        # print("array:",C_array)
    C_array=C_array.reshape(kernel,3)
    return C_array,label



Bigdata=pd.read_csv('./brake_data_events.csv')
Bigdata=Bigdata.sort_values(by=["time"],ascending=True)
Bigdata=Bigdata[['v_Vel','v_Acc','Time_Headway']]
Bigdata_size=len(Bigdata)
n=500
ID=0
Threshold=0.08
count=0
mu=1

for i in range (0,Bigdata_size-n):#遍历所有数据
    
    count+=1
    data_prior=Bigdata[ID:ID+n]
    data_current=Bigdata[i:i+n]#获取当前数据和滑动窗口数据

    data_point=Bigdata[i+n,:]#获取流进来的数据点
    data_point=data_point.reshape(1,3)
    # print(data_prior)
    # print(type(data_point))
    js_score=0
    if count%200==0:
        js_score=factor_generator_kl(data_prior,data_current)

    if js_score >Threshold:
        mu=1
        count=1
        ID=i
        print(ID)
        print("run")
        k=updata_centroid_k(data_current)
        C_array=update_centroid_position(data_current,k)
        centroid_label=find_clusters(C_array,data_point)
        label_add=np.append(label_add,centroid_label)

    else:

        if count>n:
            mu=1
            count=1
            ID=i
            print(ID)
            # print(data_current)
            k=updata_centroid_k(data_current)
            C_array=update_centroid_position(data_current,k)
            centroid_label=find_clusters(C_array,data_point)
            label_add=np.append(label_add,centroid_label)

        else:
            centroid_label=find_clusters(C_array,data_point)
            label_add=np.append(label_add,centroid_label)
