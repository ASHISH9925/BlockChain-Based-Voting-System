const web3 = new Web3("http://localhost:8545");

window.ready = false;
window.contractInstance = null;

// Log web3 connection status
try {
  web3.eth.net.isListening()
    .then(listening => {
      console.log("Web3 connection status:", listening ? "Connected" : "Not connected");
    })
    .catch(error => {
      console.error("Web3 connection error:", error.message);
    });
} catch (error) {
  console.error("Failed to check Web3 connection:", error.message);
}

// Initialize contract
fetch("/static/truffle/build/contracts/ClassVoting.json")
  .then(response => {
    if (!response.ok) {
      throw new Error(`Failed to fetch contract: ${response.status} ${response.statusText}`);
    }
    return response.json();
  })
  .then(async contract => {
    try {
      const networkId = await web3.eth.net.getId();
      console.log("Connected to network ID:", networkId);
      
      const deployedNetwork = contract.networks[networkId];
      if (!deployedNetwork || !deployedNetwork.address) {
        throw new Error(`Contract not deployed on network ID ${networkId}`);
      }
      console.log("Contract address:", deployedNetwork.address);
      const contractInstance = new web3.eth.Contract(contract.abi, deployedNetwork.address);
      window.contractInstance = contractInstance;
      window.ready = true;
      console.log("Contract initialized successfully");
    } catch (error) {
      console.error("Contract initialization error:", error.message);
    }
  })
  .catch(error => {
    console.error("Contract loading error:", error.message);
  });

class ClassVotingClient {
    constructor(web3, contractJson) {
        this.web3 = web3;
        this.contractJson = contractJson;
        this.contract = null;
    }

    async init() {
        const networkId = await this.web3.eth.net.getId();
        const deployedNetwork = this.contractJson.networks[networkId];
        if (!deployedNetwork) throw new Error("Contract not deployed on current network");

        this.contract = new this.web3.eth.Contract(
            this.contractJson.abi,
            deployedNetwork.address
        );
    }

    async getDefaultAccount() {
        const accounts = await this.web3.eth.getAccounts();
        if (!accounts.length) throw new Error("No accounts found");
        return accounts[0];
    }

    // Admin: Add candidates for a class
    async addClassCandidates(classId, candidates) {
        const from = await this.getDefaultAccount();
        return this.contract.methods.addClassCandidates(classId, candidates).send({ from });
    }

    // Admin: Register voter IDs
    async addVoters(voterIds) {
        const from = await this.getDefaultAccount();
        return this.contract.methods.addVoters(voterIds).send({ from });
    }

    // Public: Get all candidates in a class
    async candidatesOf(classId) {
        return this.contract.methods.candidatesOf(classId).call();
    }

    // Public: Get vote count for a candidate
    async getVotes(classId, candidate) {
        return this.contract.methods.getVotes(classId, candidate).call();
    }

    // Public: Vote for a candidate in a class
    async vote(classId, candidate, voterId) {
        const from = await this.getDefaultAccount();
        return this.contract.methods.vote(classId, candidate, voterId).send({ from });
    }
}


