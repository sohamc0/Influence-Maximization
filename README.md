# Influence Maximization using Degree Heuristics for Independent Cascade Models
Influence Maximization is a problem that needs to be solved in various fields. If you are looking to get exposure to your brand's product, for example, intuitively, you will look to contact the social media accounts, within the relevant industry, which has the highest number of followers. Another instance where a solution to this problem may be utilized is finding the most critical station for routing internet traffic. 

In the first example, a directed graph would be appropriate since the action of "following" an account is not necessarily bidirectional. However, in the latter example, internet traffic occurs both ways between 2 adjacent stations in a network topology. Hence, an undirected graph would be appropriate. 

Although it may seem more complicated to deal with directed graphs, we focus on getting the `k` nodes, where `k` is an arbitrary integer, in a network which maximizes the number of nodes which are "influenced".

## Diffusion Model
In Twitter, when an account `A` retweets a post, all of `A`'s followers see the post and have a decision to make: retweet the post themselves or simply ignore it. The decision to retweet the post can be denoted by the probability `p`, and it counts as the account being "successfully influenced" or, more formally, activated. We will examine two diffusion models. One is where all accounts have the same probability `p` of retweeting a post. In other words, a static `p`.

The other model, will attribute a different value of `p` for various individual nodes. The value `p` of a node `N` depends on factors including, but not limited to, `N`'s immediate neighbors (in our case, followers and the accounts that `N` follows). How the value of `p` is derived for each node is further explained in this [paper](https://www.sciencedirect.com/science/article/pii/S1877050920315416). This study shows a technique to retrieve a highly capable seed set in an undirected graph. So, we build on this approach by attempting the same method on a directed graph. The dataset used is shown below.

## Dataset
The [Higgs Twitter Dataset](https://snap.stanford.edu/data/higgs-twitter.html) was used for this project. In particular, we used the `social_network` and the `retweet_network`.

## Step 1: Finding the Seed Set
How many accounts should be chosen to start the message propogation? After all, there may be higher associated costs by starting out with a larger group of accounts. This problem is addressed through adjusting the hyperparameter that denotes the size of the group of accounts that will advertise the product, known more formally as the seed set. This project's goal is to find the optimal seed set (i.e. maximizing the number of activated nodes in the social network after the application of the diffusion model) given the size of the seed set `k` and a directed graph. 

As mentioned before, the trivial solution to this problem is to select the `k` nodes with the highest degree centrality or, in a directed graph, in-degree. Historically, this set is the easiest to derive, but does not perform well when compared to seed sets derived by the CELF algorithm ([paper](https://www.cs.cmu.edu/~jure/pubs/detect-kdd07.pdf)). However, CELF takes a tremendous amount of time to compute, especially on large networks like ours. So, a nice balance was found when using the Degree Heuristics for Independent Cascade Models (DHICM) algorithm.

## Step 2: Retrieving the Results from the Independent Cascade Model (ICM)
After the DHICM algorithm returns the seed set as its output, we use that set as the input to the ICM algorithm. Here, the network will go through the diffusion model and the "message" may or may not propogate from one node to its neighbors or successors, in our case. In the end, we will get the number of activated nodes after the message propogates through the network, while adhering to the given diffusion model.

## Results for the Higgs Twitter Dataset
### Visualzation
![Different colors represent different communities in the sampled graph (40,000 nodes)](/images/graph-communities.PNG "Communities Within the Network")

### Results
With `k = 300`, p = 0.1 + (d<sub>i</sub>/d<sub>j</sub>)/n + $\frac{CN(i,j)}{n}$, where CN(i,j) is the number of common neighbors shared by nodes i and j...
| Algorithm | Average Spread Achieved |
| :-------- | :---------------------- |
| DHICM | 17,475.1 |
| Degree Centrality | 17,393.6 |

### Reproduction of Results
Detailed steps regarding applying DHICM for other networks, including the one used in this project, will be found in `/src/README.md`.
