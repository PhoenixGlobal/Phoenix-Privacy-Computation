// SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;
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

interface PHB {
    function burnFrom(address account, uint256 amount) external;
}

contract PHBSwap is Context, Ownable {
    IERC20 public CcdToken;
    PHB public PhbToken;
    uint256 public swapRate;

    constructor(address _ccdAddress,address _phbAddress,uint256 _swapRate) public  {
        CcdToken = IERC20(_ccdAddress);
        PhbToken= PHB(_phbAddress);
        swapRate = _swapRate;
    }

    event Swap(address sender,uint256 amount);

    function setPhbToken(address phbAddress) external onlyOwner{
        require(phbAddress != address(0), "ERC20: new phb address is the zero address");
        PhbToken= PHB(phbAddress);
    }

    function setCcdToken(address ccdAddress) external onlyOwner{
        require(ccdAddress != address(0), "ERC20: new ccd token address is the zero address");
        CcdToken = IERC20(ccdAddress);
    }

    function setSwapRate(uint256 rate) external onlyOwner{
        require(rate>0, "ERC20: new swapRate should be more than zero");
        swapRate = rate;
    }

    function swap(uint256 amount) external{
        PhbToken.burnFrom(_msgSender(),amount);
        CcdToken.transfer(_msgSender(),amount*swapRate);
        emit Swap(_msgSender(),amount);
    }
}