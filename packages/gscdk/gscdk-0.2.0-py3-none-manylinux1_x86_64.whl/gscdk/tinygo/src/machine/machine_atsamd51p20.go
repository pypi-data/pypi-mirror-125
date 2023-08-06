// +build sam,atsamd51,atsamd51p20

// Peripheral abstraction layer for the atsamd51.
//
// Datasheet:
// http://ww1.microchip.com/downloads/en/DeviceDoc/60001507C.pdf
//
package machine

import "device/sam"

const HSRAM_SIZE = 0x00040000

// This chip has five TCC peripherals, which have PWM as one feature.
var (
	TCC0 = (*TCC)(sam.TCC0)
	TCC1 = (*TCC)(sam.TCC1)
	TCC2 = (*TCC)(sam.TCC2)
	TCC3 = (*TCC)(sam.TCC3)
	TCC4 = (*TCC)(sam.TCC4)
)

func (tcc *TCC) configureClock() {
	// Turn on timer clocks used for TCC and use generic clock generator 0.
	switch tcc.timer() {
	case sam.TCC0:
		sam.MCLK.APBBMASK.SetBits(sam.MCLK_APBBMASK_TCC0_)
		sam.GCLK.PCHCTRL[sam.PCHCTRL_GCLK_TCC0].Set((sam.GCLK_PCHCTRL_GEN_GCLK0 << sam.GCLK_PCHCTRL_GEN_Pos) | sam.GCLK_PCHCTRL_CHEN)
	case sam.TCC1:
		sam.MCLK.APBBMASK.SetBits(sam.MCLK_APBBMASK_TCC1_)
		sam.GCLK.PCHCTRL[sam.PCHCTRL_GCLK_TCC1].Set((sam.GCLK_PCHCTRL_GEN_GCLK0 << sam.GCLK_PCHCTRL_GEN_Pos) | sam.GCLK_PCHCTRL_CHEN)
	case sam.TCC2:
		sam.MCLK.APBCMASK.SetBits(sam.MCLK_APBCMASK_TCC2_)
		sam.GCLK.PCHCTRL[sam.PCHCTRL_GCLK_TCC2].Set((sam.GCLK_PCHCTRL_GEN_GCLK0 << sam.GCLK_PCHCTRL_GEN_Pos) | sam.GCLK_PCHCTRL_CHEN)
	case sam.TCC3:
		sam.MCLK.APBCMASK.SetBits(sam.MCLK_APBCMASK_TCC3_)
		sam.GCLK.PCHCTRL[sam.PCHCTRL_GCLK_TCC3].Set((sam.GCLK_PCHCTRL_GEN_GCLK0 << sam.GCLK_PCHCTRL_GEN_Pos) | sam.GCLK_PCHCTRL_CHEN)
	case sam.TCC4:
		sam.MCLK.APBDMASK.SetBits(sam.MCLK_APBDMASK_TCC4_)
		sam.GCLK.PCHCTRL[sam.PCHCTRL_GCLK_TCC4].Set((sam.GCLK_PCHCTRL_GEN_GCLK0 << sam.GCLK_PCHCTRL_GEN_Pos) | sam.GCLK_PCHCTRL_CHEN)
	}
}

func (tcc *TCC) timerNum() uint8 {
	switch tcc.timer() {
	case sam.TCC0:
		return 0
	case sam.TCC1:
		return 1
	case sam.TCC2:
		return 2
	case sam.TCC3:
		return 3
	case sam.TCC4:
		return 4
	default:
		return 0x0f // should not happen
	}
}
