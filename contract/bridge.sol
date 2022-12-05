// SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;
import "@openzeppelin/contracts/access/Ownable.sol";

interface PHB {
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
    function burnFrom(address account, uint256 amount) external;
}

contract PHBHub is Context, Ownable {
    PHB public PhbToken;

    constructor(address _phbAddress) public  {
        PhbToken= PHB(_phbAddress);
    }

    event CrossChain(address sender,uint256 amount,address receiver);

    function crossChain(uint256 amount,address receiver) external{
        PhbToken.burnFrom(_msgSender(),amount);
        emit CrossChain(_msgSender(),amount,receiver);
    }
}
