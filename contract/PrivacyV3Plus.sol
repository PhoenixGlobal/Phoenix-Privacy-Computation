// SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;
import "@openzeppelin/contracts/utils/Strings.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

interface IERC20 {
    function totalSupply() external view returns (uint256);
    function decimals() external view returns (uint8);
    function symbol() external view returns (string memory);
    function name() external view returns (string memory);
    function getOwner() external view returns (address);
    function balanceOf(address account) external view returns (uint256);
    function transfer(address recipient, uint256 amount) external returns (bool);
    function allowance(address _owner, address spender) external view returns (uint256);
    function approve(address spender, uint256 amount) external returns (bool);
    function transferFrom(address sender, address recipient, uint256 amount) external returns (bool);
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
}

contract PrivacyComputationV3Plus is Context, Ownable {
    struct Job {
        uint256 jobId;
        mapping (string => string) resultMap;
        string jobName;
        string expression;
        uint256 roundId;
        address party0;
        address party1;
        address party2;
        address owner;
    }

    mapping (uint256 => Job) public Jobs;
    IERC20 public Ccd;
    address public ccdCollector;

    event CreateAJob(address sender,uint256 jobId,string jobName,string expression,address partyA,address partyB,address partyC);
    event UpdateAJob(address sender,uint256 jobId,string jobName,string expression,address partyA,address partyB,address partyC);
    event DeleteAJob(address sender,uint256 jobId);
    event MpcSubmit(address sender,uint256 jobId,uint256 roundId,bytes data,uint256 ccdCost);
    event StartAJob(address sender,uint256 jobId,uint256 roundId);

    constructor(address ccd,address ccdCollectorAddress) {
        Ccd = IERC20(ccd);
        ccdCollector=ccdCollectorAddress;
    }

    function setCcdCollector(address ccdCollectorAddress) external onlyOwner{
        require(ccdCollectorAddress != address(0), "ERC20: new ccdCollector address is the zero address");
        ccdCollector=ccdCollectorAddress;
    }

    function setCcd(address ccdAddress) external onlyOwner{
        require(ccdAddress != address(0), "ERC20: new ccd token address is the zero address");
        Ccd = IERC20(ccdAddress);
    }

    function createJob(string calldata jobName,string calldata expression,address partyA,address partyB,address partyC) public returns (uint256){
        require(partyA != address(0), "address partyA is the zero address");
        require(bytes(jobName).length > 0,"jobName is empty");
        require(bytes(expression).length > 0,"expression is empty");
        uint256 timestamp = block.timestamp/1000;
        uint256 jobId=getJobId(_msgSender(),timestamp);
        require(Jobs[jobId].jobId==0,"Job already exists");
        Job storage job = Jobs[jobId];
        job.jobId=jobId;
        job.jobName=jobName;
        job.expression=expression;
        job.roundId=1;
        job.party0=partyA;
        job.party1=partyB;
        job.party2=partyC;
        job.owner=_msgSender();
        emit CreateAJob(_msgSender(),jobId,jobName,expression,partyA,partyB,partyC);
        return jobId;
    }

    function updateJob(uint256 jobId,address partyA,address partyB,address partyC) external{
        Job storage job=Jobs[jobId];
        require(job.jobId != 0, "Job does not exist");
        require(_msgSender()==owner() || _msgSender()==job.owner, "You are not the owner of the job");
        require(partyA != address(0), "address partyA is the zero address");
        job.party0=partyA;
        job.party1=partyB;
        job.party2=partyC;
        emit UpdateAJob(_msgSender(),jobId,job.jobName,job.expression,partyA,partyB,partyC);
    }

    function startJob(uint256 jobId) external{
        Job storage job=Jobs[jobId];
        require(job.jobId != 0, "Job does not exist");
        require(_msgSender() == owner()|| _msgSender()==job.owner ||_msgSender()== job.party0||_msgSender()== job.party1||_msgSender()== job.party2, "caller is not the party");
        uint256 roundId = getRoundId(jobId);
        emit StartAJob(_msgSender(),jobId,roundId);
    }

    function getJobId(address owner,uint256 timestamp) public pure returns(uint256){
        return uint256(keccak256(abi.encode(owner, timestamp)));
    }

    function getSubmitKey(address sender,uint256 roundId)public pure returns(string memory){
        return string(abi.encodePacked(Strings.toHexString(uint160(sender), 20), "-",Strings.toString(roundId)));
    }

    function getSubmit(uint256 jobId,address part,uint256 roundId)public view returns(string memory){
        Job storage job=Jobs[jobId];
        require(job.jobId != 0, "Job does not exist");
        require((part== job.party0||part== job.party1||part== job.party2), "part address error");

        string memory submitKey = getSubmitKey(part,roundId);
        return job.resultMap[submitKey];
    }

    function deleteJob(uint256 jobId) external{
        Job storage job=Jobs[jobId];
        require(job.jobId != 0, "Job does not exist");
        require(_msgSender()==owner() || _msgSender()==job.owner, "You are not the owner of the job");
        delete Jobs[jobId];
        emit DeleteAJob(_msgSender(),jobId);
    }

    function mpcSubmit(uint256 jobId,uint256 roundId,bytes calldata data,uint256 ccdCost) external{
        Job storage job=Jobs[jobId];
        require(job.jobId != 0, "Job does not exist");
        require(roundId == job.roundId, "the roundId is not equal to roundId of the job");
        require((_msgSender()== job.party0||_msgSender()== job.party1||_msgSender()== job.party2), "msg.sender address error");

        string memory message = string(data);
        string memory submitKey = getSubmitKey(_msgSender(),roundId);

        require(bytes(job.resultMap[submitKey]).length == 0, "do not resubmit");

        Ccd.transferFrom(_msgSender(),ccdCollector,ccdCost);

        job.resultMap[submitKey]=message;

        bool isAllSubmit=true;
        if(job.party0!= address(0)) {
            string memory submit0=getSubmit(jobId,job.party0,roundId);
            if(bytes(submit0).length==0){
                isAllSubmit=false;
            }
        }

        if(job.party1!= address(0)) {
            string memory submit1=getSubmit(jobId,job.party1,roundId);
            if(bytes(submit1).length==0){
                isAllSubmit=false;
            }
        }

        if(job.party2!= address(0)) {
            string memory submit2=getSubmit(jobId,job.party2,roundId);
            if(bytes(submit2).length==0){
                isAllSubmit=false;
            }
        }

        if(isAllSubmit){
            job.roundId++;
        }

        emit MpcSubmit(_msgSender(),jobId,roundId,data,ccdCost);
    }

    function getRoundId(uint256 jobId) public view returns(uint256)
    {
        Job storage job=Jobs[jobId];
        require(job.jobId != 0, "Job does not exist");
        return job.roundId;
    }

    function getExpression(uint256 jobId) public view returns(string memory)
    {
        Job storage job=Jobs[jobId];
        require(job.jobId != 0, "Job does not exist");
        return job.expression;
    }

    function ReSetRoundId(uint256 jobId) external {
        Job storage job=Jobs[jobId];
        require(job.jobId != 0, "Job does not exist");
        require(_msgSender() == owner()|| _msgSender()==job.owner ||_msgSender()== job.party0||_msgSender()== job.party1||_msgSender()== job.party2, "caller is not the party");
        job.roundId++;
    }
}