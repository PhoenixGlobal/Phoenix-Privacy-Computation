// SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;
import "@openzeppelin/contracts/utils/Strings.sol";
import "@openzeppelin/contracts/access/Ownable.sol";


contract PrivacyComputationV2 is Context, Ownable {
    struct Job {
        uint256 jobId;
        mapping (string => string) resultMap;
        string jobName;
        uint256 roundId;
        address party0;
        address party1;
        address party2;
        address owner;
    }

    mapping (uint256 => Job) public Jobs;

    event CreateAJob(address sender,uint256 jobId,string jobName,address partyA,address partyB,address partyC);
    event DeleteAJob(address sender,uint256 jobId);
    event MpcSubmit(address sender,uint256 jobId,uint256 roundId,bytes data);

    constructor() public  {
    }

    function createJob(string calldata jobName,address partyA,address partyB,address partyC) public returns (uint256){
        require(partyA != address(0), "address partyA is the zero address");
        require(partyB != address(0), "address partyB is the zero address");
        require(partyC != address(0), "address partyC is the zero address");
        require(bytes(jobName).length > 0,"jobName is empty");
        uint256 timestamp = block.timestamp/1000;
        uint256 jobId=getJobId(_msgSender(),timestamp);
        require(Jobs[jobId].jobId==0,"Job already exists");
        Job storage job = Jobs[jobId];
        job.jobId=jobId;
        job.jobName=jobName;
        job.roundId=1;
        job.party0=partyA;
        job.party1=partyB;
        job.party2=partyC;
        job.owner=_msgSender();
        emit CreateAJob(_msgSender(),jobId,jobName,partyA,partyB,partyC);
        return jobId;
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
        require(job.owner != _msgSender(), "You are not the owner of the job");
        delete Jobs[jobId];
        emit DeleteAJob(_msgSender(),jobId);
    }

    function mpcSubmit(uint256 jobId,uint256 roundId,bytes calldata data) external{
        Job storage job=Jobs[jobId];
        require(job.jobId != 0, "Job does not exist");
        require(roundId == job.roundId, "the roundId is not equal to roundId of the job");
        require((_msgSender()== job.party0||_msgSender()== job.party1||_msgSender()== job.party2), "msg.sender address error");

        string memory message = string(data);
        string memory submitKey = getSubmitKey(_msgSender(),roundId);

        require(bytes(job.resultMap[submitKey]).length == 0, "do not resubmit");
        job.resultMap[submitKey]=message;

        string memory submit0=getSubmit(jobId,job.party0,roundId);
        string memory submit1=getSubmit(jobId,job.party1,roundId);
        string memory submit2=getSubmit(jobId,job.party2,roundId);
        if(bytes(submit0).length>0 && bytes(submit1).length > 0 && bytes(submit2).length > 0){
            job.roundId++;
        }
        emit MpcSubmit(_msgSender(),jobId,roundId,data);
    }


    function getRoundId(uint256 jobId) external view returns(uint256)
    {
        Job storage job=Jobs[jobId];
        require(job.jobId != 0, "Job does not exist");
        return job.roundId;
    }

    function ReSetRoundId(uint256 jobId) external {
        Job storage job=Jobs[jobId];
        require(job.jobId != 0, "Job does not exist");
        require(_msgSender() == owner()||_msgSender()== job.party0||_msgSender()== job.party1||_msgSender()== job.party2, "caller is not the party");
        job.roundId++;
    }
}